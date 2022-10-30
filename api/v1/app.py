#!/usr/bin/env python3
"""Entry point for HolbertonBnB API calls."""
from os import getenv
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flasgger import Swagger, swag_from
from models import storage
from api.v1.views import app_views

# Flask configuration
app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

# Flasgger configuration
template = {
    "swagger": "2.0",
    "info": {
        "title": "HolbertonBnB",
        "description": "RESTful API for HolbertonBnB",
    }
}
# Externally load Swagger static content
swagger_config = Swagger.DEFAULT_CONFIG
swagger_config['swagger_ui_bundle_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
swagger_config['swagger_ui_standalone_preset_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
swagger_config['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
swagger_config['swagger_ui_css'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'
swagger = Swagger(app, template=template)


@app.errorhandler(404)
def not_found(error):
    """Returns a JSON-formatted 404 status code response."""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_storage(exc):
    """Closes the storage session after every request."""
    storage.close()


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", default="0.0.0.0"),
        port=getenv("HBNB_API_PORT", default="5000"),
        threaded=True
    )
