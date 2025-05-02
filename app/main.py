from flask import Flask
from content_api import content_bp # correct if content_api.py is in the same folder

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(content_bp)


# Define Home route
@app.route('/')
def home():
    return {"message": "Welcome to the API Home!"}

if __name__ == '__main__':
    app.run(debug=True)
