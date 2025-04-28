from flask import Flask
from content_api import content_bp

app = Flask(__name__)

# Register routes
app.register_blueprint(content_bp)

if __name__ == '__main__':
    app.run(debug=True)
