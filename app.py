from flask import Flask
from flask_cors import CORS
from api.recipes import get_recipes_blueprint

app = Flask(__name__)

CORS(app)

# Register the blueprint from the API folder
app.register_blueprint(get_recipes_blueprint)

@app.route('/')
def home():
    return "Welcome to the Grocery-to-Recipe App!"

if __name__ == '__main__':
    app.run(debug=True)