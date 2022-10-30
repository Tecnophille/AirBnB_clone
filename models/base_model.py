#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Base Model Module

This module is in charge of establishing a reference
Base Model for the rest of the classes of the
HBNB project (Airbnb Clone), from which it will be possible
to extract information such as: A unique universal identifier,
the date and time in which a class was created and updated,
a standard format to print the class content, a way to save
the data created from the instances and finally the representation
of all the keys and values of an instance.

"""

from datetime import datetime
import models
import uuid


class BaseModel:
    """Base Model Class

    This is the Base Model that take care of the
    initialization, serialization and deserialization
    of the future instances.

    Attributes:
        id (str): It's an UUID for when an instance is created.
        created_at (datetime): The current date and time that
            an instance is created.
        updated_at (datetime): The current date and time that
            an instance is created and it will be updated every
            time that the object changes.

    """

    def __init__(self, *args, **kwargs):
        """Base Model __init__ Method

        Here, the default values of a Base Model
        instance are initialized.

        """
        if kwargs:
            for arg, val in kwargs.items():
                if arg in ('created_at', 'updated_at'):
                    val = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S.%f')

                if arg != '__class__':
                    setattr(self, arg, val)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """Representation of the class for the user

        Example:
            $ bm = BaseModel()
            $ print(bm)

            This method prints the content of the Base Model
            class with this format

            $ [<class name>] (<self.id>) <self.__dict__>

        """
        return '[{0}] ({1}) {2}'.format(
                self.__class__.__name__, self.id, self.__dict__
            )

    def save(self):
        """Updates a Base Model instance

        Updates the public instance attribute `updated_at`
        with the current datetime and dumps the class data
        into a file

        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Converts the information of the class to human-readable format

        Returns a new dictionary containing all keys/values
        of __dict__ of the instance.

        """
        class_info = self.__dict__.copy()
        class_info['__class__'] = self.__class__.__name__
        class_info['created_at'] = self.created_at.isoformat()
        class_info['updated_at'] = self.updated_at.isoformat()

        return class_info
