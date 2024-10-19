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

    # Call the OpenAI API
    prompt = f"Generate recipes using the following groceries: {grocery_list}"
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        
        recipes = response.choices[0].text.strip()
        return jsonify({"recipes": recipes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500