import os
import json
import asyncio
from concurrent.futures import TimeoutError
from dotenv import load_dotenv  # Load .env file support
from pydantic import BaseModel, ValidationError
from typing import Any, Dict, List, Callable
import google.generativeai as genai

# --------------------------------
# Load environment variables
# --------------------------------
load_dotenv()  # Reads .env from current directory

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise EnvironmentError(
        "Please set GEMINI_API_KEY in your .env file, e.g.:\n"
        "GEMINI_API_KEY=your_api_key_here"
    )
# Dish to process
Dish = "Sugar free cookies"

# --------------------------------
# Initialize Gemini client
# --------------------------------
genai.configure(api_key=gemini_api_key)

# --------------------------------
# Tool Registry
# --------------------------------
tool_registry: Dict[str, Callable] = {}

def agentic_tool(name: str):
    def decorator(func: Callable):
        tool_registry[name] = func
        return func
    return decorator

# --------------------------------
# Data Models
# --------------------------------
class Recipe(BaseModel):
    recipe_name: str
    ingredients: List[str]
    cooking_style: str
    glycemic_load: float

class AgentAction(BaseModel):
    name: str
    parameters: Dict[str, Any]

# --------------------------------
# Tool Implementations
# --------------------------------
@agentic_tool("get_ingredients")
def get_ingredients(recipe: Recipe) -> List[str]:
    return recipe.ingredients

@agentic_tool("calculate_glycemic_load")
def calculate_glycemic_load(recipe: Recipe) -> float:
    return recipe.glycemic_load

# --------------------------------
# Prompt Templates
# --------------------------------
system_prompt = f"""
You are a recipe agent. Given a dish name, fetch recipe details (recipe_name, ingredients, cooking_style, glycemic_load) in JSON. Use tools when needed:
- get_ingredients(recipe)
- calculate_glycemic_load(recipe)
Respond with either:
FUNCTION_CALL: <tool_name>|<param1>|...
or
FINAL_ANSWER: <JSON>
"""
user_query = f"Fetch recipe for '{Dish}' and output JSON or call tools accordingly."

# --------------------------------
# LLM Invocation
# --------------------------------
async def call_gemini(messages: List[Dict[str, str]]) -> str:
    gemini_messages = []
    system_instruction = None
    for msg in messages:
        role = msg["author"]
        if role == "system":
            system_instruction = msg["content"]
            continue
        gemini_messages.append(
            {"role": "model" if role == "assistant" else "user", "parts": [msg["content"]]}
        )

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", system_instruction=system_instruction
    )
    resp = await model.generate_content_async(gemini_messages)
    return resp.text.strip()

# --------------------------------
# Agent Loop
# --------------------------------
async def main():
    messages = [
        {"author":"system","content":system_prompt},
        {"author":"user","content":user_query}
    ]
    # First call
    response = await call_gemini(messages)
    print(f"LLM: {response}\n")

    # If function call, execute and ask for final
    if response.startswith("FUNCTION_CALL:"):
        _, call = response.split("FUNCTION_CALL:",1)
        parts = call.split("|")
        fname = parts[0].strip()
        args = parts[1:]
        # placeholder recipe stub for tool
        stub = {"recipe_name":Dish, "ingredients":["..."], "cooking_style":"...", "glycemic_load":0}
        recipe = Recipe(**stub)
        result = tool_registry[fname](recipe)
        print(f"Executed {fname}, result: {result}\n")
        # ask for final answer
        messages.append({"author":"assistant","content":response})
        messages.append({"author":"user","content":f"The result for {fname} is {result}. Provide FINAL_ANSWER JSON with recipe and actions."})
        final = await call_gemini(messages)
        print(f"LLM Final: {final}\n")
        response = final

    # Parse FINAL_ANSWER JSON
    if response.startswith("FINAL_ANSWER:"):
        _, j = response.split("FINAL_ANSWER:",1)
        data = json.loads(j)
        recipe = Recipe(**data['recipe'])
        # Print nicely
        print(f"Recipe Name   : {recipe.recipe_name}")
        print(f"Ingredients   : {', '.join(recipe.ingredients)}")
        print(f"Cooking Style : {recipe.cooking_style}")
        print(f"Glycemic Load : {recipe.glycemic_load}")
        print("----------------------------------------")

if __name__ == "__main__":
    asyncio.run(main())
