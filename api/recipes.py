from flask import Blueprint, request, jsonify

get_recipes_blueprint = Blueprint('get_recipes', __name__)

@get_recipes_blueprint.route('/get-recipes', methods=['POST'])
def get_recipes():
    groceries = request.json.get('groceries', [])
    if not groceries:
        return jsonify({"error": "No groceries provided"}), 400

    # Placeholder for calling OpenAI API (or logic to generate recipes)
    # You can add logic here to process the groceries and return recipes
    recipes = generate_recipes_from_groceries(groceries)
    return jsonify({"recipes": recipes})

def generate_recipes_from_groceries(groceries):
    # Dummy function that returns example recipes based on the provided groceries
    # This will later be replaced with logic to call OpenAI or other APIs
    return [f"Recipe using {ingredient}" for ingredient in groceries]