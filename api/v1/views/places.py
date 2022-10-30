#!/usr/bin/env python3
"""HolbertonBnB Place view."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger import swag_from
from models import storage
from models.place import Place
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"])
@swag_from("../apidocs/places/get_places.yml", methods=["GET"])
@swag_from("../apidocs/places/post.yml", methods=["POST"])
def places(city_id):
    """Defines the GET and POST method for places on /cities route.

    GET - Retrieves a list of all Places related to a given city_id.
    POST - Creates a Place.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    # GET method
    if request.method == "GET":
        return jsonify([p.to_dict() for p in city.places])

    # POST method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    user_id = data.get("user_id")
    if user_id is None:
        return "Missing user_id", 400
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if data.get("name") is None:
        return "Missing name", 400
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"])
@swag_from("../apidocs/places/get_place_id.yml", methods=["GET"])
@swag_from("../apidocs/places/delete.yml", methods=["DELETE"])
@swag_from("../apidocs/places/put.yml", methods=["PUT"])
def place_id(place_id):
    """Defines the GET, PUT and DELETE methods for a specific ID on places.

    GET - Retrieves a Place object with the given id.
    PUT - Updates a Place object with the given id using JSON key/values.
    DELETE - Deletes a Place object with the given id.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    # GET method
    if request.method == "GET":
        return jsonify(place.to_dict())

    # DELETE method
    elif request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({})

    # PUT method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    avoid = {"id", "user_id", "city_id", "created_at", "updated_at"}
    [setattr(place, k, v) for k, v in data.items() if k not in avoid]
    place.save()
    return jsonify(place.to_dict())


@app_views.route("/places_search", methods=["POST"])
@swag_from("../apidocs/places/search.yml")
def places_search():
    """Retrives Place objects depending on the JSON request data."""
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if len(data) == 0 or all(len(l) == 0 for l in data.values()):
        return jsonify([p.to_dict() for p in storage.all("Place").values()])

    places = []

    states = data.get("states")
    if states is not None and len(states) != 0:
        for s in states:
            state = storage.get("State", s)
            if state is not None:
                [[places.append(p) for p in c.places] for c in state.cities]

    cities = data.get("cities")
    if cities is not None and len(cities) != 0:
        for c in cities:
            city = storage.get("City", c)
            if city is not None:
                [places.append(p) for p in city.places]

    amenities = data.get("amenities")
    place_amenities = []
    if amenities is not None and len(amenities) != 0:
        for p in storage.all("Place").values():
            if type(storage) == DBStorage:
                amenity_ids = [a.id for a in p.amenities]
            else:
                amenity_ids = p.amenity_ids
            if set(amenities).issubset(set(amenity_ids)):
                p.__dict__.pop("amenities", None)
                p.__dict__.pop("amenity_ids", None)
                place_amenities.append(p)
        if len(places) != 0:
            places = list(set(places) & set(place_amenities))
        else:
            places = place_amenities

    return jsonify([p.to_dict() for p in places])
