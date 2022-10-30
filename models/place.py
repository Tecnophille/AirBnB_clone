#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Place Module

This Module inherits from BaseModel class.
Place Module contains the attributes to be assigned
to the Places created.
"""

from models.base_model import BaseModel


class Place(BaseModel):
    """Place Class

    Attributes:
        city_id (str): The UUID of the City the Place is located in
        user_id (str): The UUID of the User of the Place
        name (str): The Place name
        description (str): The Place description
        number_rooms (int): The number of rooms in the Place
        number_bathrooms (int): The number of bathrooms in the Place
        max_guest (int): The maximum number of guests for the Place
        price_by_night (int): The price per night
        latitude (float): The latitude of the Place
        longitude (float): The longitude of the Place
        amenity_ids (list): A list that contains all the Amenities in the Place

    """
    city_id = ''
    user_id = ''
    name = ''
    description = ''
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
