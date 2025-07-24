import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_smorest import Api
from dotenv import load_dotenv

from .models import db
from .routes.health import blp as health_blp
from .routes.events import blp as events_blp

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.url_map.strict_slashes = False

# Configure from .env or use SQLite fallback
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///events.db")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Flask-Smorest/OpenAPI config
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["API_TITLE"] = "My Flask API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Initialize extensions
db.init_app(app)
api = Api(app)

# Register blueprints
api.register_blueprint(health_blp)
api.register_blueprint(events_blp)

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad Request", "message": str(e)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found", "message": str(e)}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

def setup_database(app):
    """Helper to create tables if not exist."""
    with app.app_context():
        db.create_all()

# Ensure tables exist on startup (not for production scale)
setup_database(app)
