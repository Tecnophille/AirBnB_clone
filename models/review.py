#!/usr/bin/python3
""" holds class Review"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey

class Review(BaseModel, Base):
    """Representation of Review """
    if models.storage_t == 'db':
        _tablename_ = 'reviews'
        place_id = Column(String(60))
ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60))
ForeignKey('users.id'), nullable=False)
        Text = Column(String(1024), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    def_init_(self, args, *kwargs):
        """initializes Review"""
        super()._init_(args, *kwargs)
        