#!/usr/bin/env python3
"""HolbertonBnB main Flask application.

The application listens on host IP 0.0.0.0, port 5000.
Routes:
    /hbnb: HBnB home page.
"""
import uuid
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session after each request."""
    storage.close()


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Displays the main HBnB filters home page."""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    places = storage.all("Place")
    cache_id = (str(uuid.uuid4()))
    return render_template("index.html",
                           states=states,
                           amenities=amenities,
                           places=places,
                           cache_id=cache_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
