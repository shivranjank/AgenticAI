# Recipe Agent Workflow

This document outlines the step-by-step execution flow of the Gemini Recipe Agent.

```
[ Start ]
    |
    |  - User runs `python RecipeAgent1.py`
    v
[ Initialize Agent ]
    |
    |  - Set up message history with system and user prompts.
    v
[ Call Gemini API (1st time) ]
    |
    |  - Send initial request to the LLM.
    v
< Is response a FUNCTION_CALL? >
    |
    |---- [ YES ] ----> [ Parse Tool Call ]
    |                     |
    |                     |  - Extract tool name ('get_recipes') and parameters.
    |                     v
    |                   [ Execute Tool ]
    |                     |
    |                     |  - Look up 'get_recipes' in tool_registry and run it.
    |                     |  - The tool returns a list of recipe data.
    |                     v
    |                   [ Update Message History ]
    |                     |
    |                     |  - Append the tool's output to the conversation.
    |                     v
    |                   [ Call Gemini API (2nd time) ]
    |                     |
    |                     |  - Ask the LLM to format the data into the final JSON.
    |                     v
    |                   [ Receive FINAL_ANSWER ]
    |
    |
    |---- [ NO ] ------> [ Receive FINAL_ANSWER ]
    |
    v
[ Parse Final Answer JSON ]
    |
    |  - Load the JSON string from the LLM's response.
    |  - Validate the data using the `RecipeList` Pydantic model.
    v
[ Print Formatted Recipes ]
    |
    |  - Loop through each recipe in the list.
    |  - Print the name, ingredients, cooking style, and glycemic load.
    v
[ End ]
``` 