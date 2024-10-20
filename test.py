if __name__ == "__main__":
    # Simulate request data for debugging
    from flask import json

    # Simulated input for testing
    test_data = {
        "groceries": [
            {"name": "potatoes", "quantity": 6},
            {"name": "eggplants", "quantity": 2},
            {"name": "carrots", "quantity": 1},
            {"name": "bell peppers", "quantity": 6},
            {"name": "pork loin", "quantity": 1}
        ],
        "num_people": 2
    }

    # Convert test data to JSON
    test_json = json.dumps(test_data)
    
    # Simulate a POST request
    with get_recipes_blueprint.test_request_context(
            '/get-recipes', 
            method='POST', 
            data=test_json, 
            content_type='application/json'):
        print(get_recipes())  # Call the function and print the output