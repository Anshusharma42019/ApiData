from flask import Flask
from content_api import content_bp

from auth_api import auth_bp

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(content_bp)
app.register_blueprint(auth_bp)


# Define Home route
@app.route('/')
def home():
    return {"message": "Welcome to the API Home!"}

if __name__ == '__main__':
    app.run(debug=True)
