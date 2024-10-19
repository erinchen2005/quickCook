import openai
import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

get_recipes_blueprint = Blueprint('get_recipes', __name__)

@get_recipes_blueprint.route('/get-recipes', methods=['POST'])
def get_recipes():
    groceries = request.json.get('groceries', [])
    if not groceries:
        return jsonify({"error": "No groceries provided"}), 400

    # Prepare the groceries list for the OpenAI API prompt
    grocery_list = ", ".join([f"{item['quantity']} {item['name']}" for item in groceries])
    num_people = request.json.get('num_people', 1)  # Default to 1 if not provided

    # Call the OpenAI API
    prompt = f"I have the following ingredients: {grocery_list}. I am cooking for {num_people} people. 
    Please provide recipes using these ingredients, and specify how many meals I can make from them. Do not include any addition text of punctuation."
    
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150
        )
        
        recipes = response.choices[0].text.strip()
        return jsonify({"recipes": recipes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500