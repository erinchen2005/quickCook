from openai import OpenAI
import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

get_recipes_blueprint = Blueprint('get_recipes', __name__)

@get_recipes_blueprint.route('/get-recipes', methods=['POST'])
def get_recipes():
    groceries_input = request.json.get('groceries', "")
    num_people = request.json.get('num_people', 1)

    if not groceries_input:
        return jsonify({"error": "No groceries provided"}), 400

    # Process the input: Convert comma-separated grocery items into a list
    groceries_list = [item.strip() for item in groceries_input.split(',')]

    # Join the grocery list for the API prompt
    grocery_list_str = ", ".join(groceries_list)
    
    # Create the prompt
    prompt = f"I have the following ingredients: {grocery_list_str}. I am cooking for {num_people} people. Please provide recipes using these ingredients, and specify how many meals I can make from them."

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
        )
        
        raw_recipes = chat_completion.choices[0].message.content.strip()
        # Assuming you have a parsing function, otherwise the raw_recipes is the output.
        return jsonify({"recipes": raw_recipes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def test_get_recipes():
    # Simulated data
    groceries = [
        {"name": "potatoes", "quantity": 6},
        {"name": "eggplants", "quantity": 2},
        {"name": "carrots", "quantity": 1},
        {"name": "bell peppers", "quantity": 6},
        {"name": "pork loin", "quantity": 1}
    ]
    num_people = 2

    # Prepare grocery list
    grocery_list = ", ".join([f"{item['quantity']} {item['name']}" for item in groceries])
    prompt = f"""
I have the following ingredients: {grocery_list}. I am cooking for {num_people} people. 
Please provide multiple recipes using these ingredients. Each recipe should use a subset of the ingredients, not all of them, so that multiple meals can be made out of the groceries, unless the ingredients are too few and are only enough for one meal for the number of people given.
Please format the output as follows:
- Recipe Title
- Ingredients, including quantity (list each ingredient on a new line)
- Instructions (list steps numerically)
- Number of servings

Make sure the format is exactly as shown above.
"""

    try:
        # OpenAI API call
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
        )
        
        recipes = chat_completion['choices'][0]['message']['content'].strip()
        print({"recipes": recipes})

    except Exception as e:
        print({"error": str(e)})

# Run the test
test_get_recipes()