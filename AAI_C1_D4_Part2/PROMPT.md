# LLM Prompts for Building the Gemini Recipe Agent

This document provides a series of structured prompts to guide a Large Language Model (LLM) in generating the `RecipeAgent1.py` script from scratch. The prompts are broken down into logical steps, building upon each other to create the final application.

---

### Step 1: Initial Setup and Dependencies

**Prompt:**
"Create a Python script named `RecipeAgent1.py`. Start by importing the necessary libraries: `os` for environment variables, `json` for data handling, `asyncio` for asynchronous operations, `pydantic` for data modeling, `google.generativeai as genai`, and `python-dotenv` to load a `.env` file. Add the code to load environment variables and retrieve a `GEMINI_API_KEY`, raising an error if it's not found."

---

### Step 2: Data Modeling with Pydantic

**Prompt:**
"Define the data structures for our recipe agent using Pydantic. Create a `Recipe` model with the following fields: `recipe_name` (str), `ingredients` (List[str]), `cooking_style` (str), and `glycemic_load` (float). Then, create a `RecipeList` model that contains a single field, `recipes`, which is a `List[Recipe]`."

---

### Step 3: Tool Implementation

**Prompt:**
"Implement a simple tool-calling framework. First, create a global dictionary called `tool_registry`. Second, define a decorator function called `agentic_tool` that takes a tool name as an argument and registers any function it decorates into the `tool_registry`.

Finally, create a function called `get_recipes` that accepts a `dish_name` (str) and returns a hardcoded list of three sample sugar-free biscuit recipes. This function should be decorated with `@agentic_tool('get_recipes')` to register it as a tool."

---

### Step 4: System and User Prompts

**Prompt:**
"Define the instructional prompts for the LLM. Create a `system_prompt` string that instructs the agent on its role, the tools it has available (`get_recipes`), and the two possible response formats: `FUNCTION_CALL: <tool_name>|<parameter>` or `FINAL_ANSWER: <JSON_object>`.

Also, define a `user_query` string that asks the agent to fetch recipes for a specific dish, like 'sugar-free biscuits'."

---

### Step 5: Asynchronous LLM Invocation

**Prompt:**
"Write an asynchronous function `call_gemini` that takes a list of messages as input. Inside this function, configure the `genai` model for 'gemini-1.5-flash'. Convert the input message list into the format required by the Gemini API, separating the system instruction from the user/assistant messages. The function should then call the model asynchronously and return the stripped text content of the response."

---

### Step 6: The Main Agent Loop

**Prompt:**
"Create the main asynchronous function `main()`. This function should orchestrate the agent's logic:
1.  Initialize the message history with the system and user prompts.
2.  Make an initial `await` call to `call_gemini`.
3.  Check if the response is a `FUNCTION_CALL`. If so, parse the tool name and arguments, execute the corresponding function from the `tool_registry`, and append the function's output to the message history. Then, make a second `await` call to `call_gemini` to get the final answer.
4.  Check if the response is a `FINAL_ANSWER`. If so, parse the JSON content, iterate through the list of recipes, and print each one to the console in a clean, readable format."

---

### Step 7: Execution Block

**Prompt:**
"Finally, add the standard Python entry point `if __name__ == '__main__':` to run the `main` asynchronous function using `asyncio.run()`." 