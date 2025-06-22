# Gemini Recipe Agent

This project demonstrates a simple, AI-powered agent that fetches recipes for a given dish using the Google Gemini API. The agent is built with Python and uses `uv` for package management.

## Features

- **AI-Powered**: Leverages the Gemini 1.5 Flash model to understand and process recipe requests.
- **Tool-Based**: Uses a simple tool-calling framework to extend its capabilities.
- **Asynchronous**: Built with Python's `asyncio` for non-blocking I/O.
- **Pydantic Models**: Ensures data validation and structured output.

## Project Structure

```
.
├── .env.example
├── RecipeAgent1.py
└── README.md
```

## Installation Guide

Follow these steps to set up and run the Recipe Agent on your local machine.

### 1. Prerequisites

- **Python**: Make sure you have Python 3.9 or newer installed.
- **Git**: Required for cloning the repository.
- **Google Gemini API Key**: You'll need an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Initial Setup

First, clone the repository or set up your project directory with the `RecipeAgent1.py` file.

### 3. Install `uv`

This project uses `uv` as a fast and efficient package manager. If you don't have it installed, you can install it with `pip`:

```bash
pip install uv
```

### 4. Initialize Virtual Environment

Navigate to your project directory in the terminal and initialize a new virtual environment using `uv`:

```bash
uv init
```

This command will create a new virtual environment in the `.venv` directory.

### 5. Install Dependencies

Next, install the required Python packages using `uv add`. These packages are essential for running the agent:

```bash
# For making API calls to Google Gemini
uv add google-generativeai

# For environment variable management
uv add python-dotenv

# For data validation
uv add pydantic
```

### 6. Configure Environment Variables

The agent requires a Gemini API key to function.

1.  Create a new file named `.env` in the root of your project directory.
2.  Add your API key to the `.env` file as shown below:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual Google Gemini API key.

## How to Run the Agent

Once you've completed the setup, you can run the agent using the `uv run` command:

```bash
uv run python RecipeAgent1.py
```

## Expected Output

A successful run will produce the following output, showcasing the agent's ability to fetch and format multiple recipes:

```
LLM: FUNCTION_CALL: get_recipes|sugar-free biscuits

Searching for recipes for 'sugar-free biscuits'...
Executed get_recipes, result: [{'recipe_name': 'Almond Flour Cheddar Biscuits', 'ingredients': ['2 cups almond flour', ...], 'cooking_style': 'Baking', 'glycemic_load': 5.0}, ...]

LLM Final: FINAL_ANSWER: {
 "recipes": [
  {
   "recipe_name": "Almond Flour Cheddar Biscuits",
   "ingredients": [
    "2 cups almond flour",
    "1 tbsp baking powder",
    "1/2 tsp salt",
    "1/4 cup cold butter, cubed",
    "1 cup shredded sharp cheddar cheese",
    "1/2 cup unsweetened almond milk",
    "1 large egg"
   ],
   "cooking_style": "Baking",
   "glycemic_load": 5
  },
  {
   "recipe_name": "Coconut Flour Drop Biscuits",
   "ingredients": [
    "1/2 cup coconut flour",
    "1/4 cup psyllium husk powder",
    "1 tbsp baking powder",
    "1/2 tsp salt",
    "1/4 cup melted butter or coconut oil",
    "3 large eggs",
    "1/2 cup unsweetened almond milk"
   ],
   "cooking_style": "Baking",
   "glycemic_load": 6
  },
  {
   "recipe_name": "Cream Cheese Biscuits",
   "ingredients": [
    "4 oz cream cheese, softened",
    "1/2 cup unsalted butter, softened",
    "2 large eggs",
    "1 1/2 cups almond flour",
    "1 tbsp baking powder",
    "1/2 tsp salt"
   ],
   "cooking_style": "Baking",
   "glycemic_load": 4
  }
 ]
}


Recipe Name   : Almond Flour Cheddar Biscuits
Ingredients   : 2 cups almond flour, 1 tbsp baking powder, 1/2 tsp salt, 1/4 cup cold butter, cubed, 1 cup shredded sharp cheddar cheese, 1/2 cup unsweetened almond milk, 1 large egg
Cooking Style : Baking
Glycemic Load : 5.0
----------------------------------------
Recipe Name   : Coconut Flour Drop Biscuits
Ingredients   : 1/2 cup coconut flour, 1/4 cup psyllium husk powder, 1 tbsp baking powder, 1/2 tsp salt, 1/4 cup melted butter or coconut oil, 3 large eggs, 1/2 cup unsweetened almond milk
Cooking Style : Baking
Glycemic Load : 6.0
----------------------------------------
Recipe Name   : Cream Cheese Biscuits
Ingredients   : 4 oz cream cheese, softened, 1/2 cup unsalted butter, softened, 2 large eggs, 1 1/2 cups almond flour, 1 tbsp baking powder, 1/2 tsp salt
Cooking Style : Baking
Glycemic Load : 4.0
----------------------------------------
