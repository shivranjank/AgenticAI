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
Dish = "sugar-free biscuits"

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

class RecipeList(BaseModel):
    recipes: List[Recipe]

# --------------------------------
# Tool Implementations
# --------------------------------
@agentic_tool("get_recipes")
def get_recipes(dish_name: str) -> List[Dict]:
    """Fetches a list of recipes for a given dish."""
    print(f"Searching for recipes for '{dish_name}'...")
    # In a real app, this would be a database or API call.
    return [
        {
            "recipe_name": "Almond Flour Cheddar Biscuits",
            "ingredients": ["2 cups almond flour", "1 tbsp baking powder", "1/2 tsp salt", "1/4 cup cold butter, cubed", "1 cup shredded sharp cheddar cheese", "1/2 cup unsweetened almond milk", "1 large egg"],
            "cooking_style": "Baking",
            "glycemic_load": 5.0
        },
        {
            "recipe_name": "Coconut Flour Drop Biscuits",
            "ingredients": ["1/2 cup coconut flour", "1/4 cup psyllium husk powder", "1 tbsp baking powder", "1/2 tsp salt", "1/4 cup melted butter or coconut oil", "3 large eggs", "1/2 cup unsweetened almond milk"],
            "cooking_style": "Baking",
            "glycemic_load": 6.0
        },
        {
            "recipe_name": "Cream Cheese Biscuits",
            "ingredients": ["4 oz cream cheese, softened", "1/2 cup unsalted butter, softened", "2 large eggs", "1 1/2 cups almond flour", "1 tbsp baking powder", "1/2 tsp salt"],
            "cooking_style": "Baking",
            "glycemic_load": 4.0
        }
    ]

# --------------------------------
# Prompt Templates
# --------------------------------
system_prompt = f"""
You are a recipe agent. Given a dish name, your goal is to provide a list of recipes.
The final output should be a JSON object with a "recipes" key, which contains a list of recipe objects.
You have one tool available:
- get_recipes(dish_name: str): Fetches a list of recipes.

Your response should be one of two things:
1. A function call to the available tool, formatted as:
FUNCTION_CALL: <tool_name>|<parameter>

2. The final answer in JSON format, prefixed with "FINAL_ANSWER:", like this:
FINAL_ANSWER: {{"recipes": [...]}}
"""
user_query = f"Fetch recipes for '{Dish}'."

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
        args = [p.strip() for p in parts[1:]]
        
        if fname in tool_registry:
            result = tool_registry[fname](*args)
            print(f"Executed {fname}, result: {result}\n")
            # ask for final answer
            messages.append({"author":"assistant","content":response})
            messages.append({"author":"user","content":f"The result for {fname} is {json.dumps(result)}. Provide the FINAL_ANSWER in JSON format."})
            final = await call_gemini(messages)
            print(f"LLM Final: {final}\n")
            response = final
        else:
            print(f"Error: Tool '{fname}' not found.")
            return

    # Parse FINAL_ANSWER JSON
    if response.startswith("FINAL_ANSWER:"):
        _, j = response.split("FINAL_ANSWER:",1)
        data = json.loads(j)
        recipe_list = RecipeList(**data)
        for recipe in recipe_list.recipes:
            # Print nicely
            print(f"Recipe Name   : {recipe.recipe_name}")
            print(f"Ingredients   : {', '.join(recipe.ingredients)}")
            print(f"Cooking Style : {recipe.cooking_style}")
            print(f"Glycemic Load : {recipe.glycemic_load}")
            print("----------------------------------------")

if __name__ == "__main__":
    asyncio.run(main())
