#!/usr/bin/python3
"""
This module defines the main application for the AirBnB clone project.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage


app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for all origins
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Register the Blueprint containing API routes and views
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage_connection(exception):
    """
    Teardown function to close the storage connection.
    """
    storage.close()


@app.errorhandler(404)
def handle_404_error(exception):
    """
    Error handler for handling 404 errors (Not Found).
    Returns a JSON response with an error message.
    """
    error_data = {
        "error": "Not found"
    }

    response = jsonify(error_data)
    response.status_code = 404

    return response


if __name__ == "__main__":
    # Run the Flask application with host and port specified in environment
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
