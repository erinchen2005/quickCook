from flask import Flask
from api.recipes import get_recipes_blueprint

app = Flask(__name__)

# Register the blueprint from the API folder
app.register_blueprint(get_recipes_blueprint)

@app.route('/')
def home():
    return "Welcome to the Grocery-to-Recipe App!"

if __name__ == '__main__':
    app.run(debug=True)