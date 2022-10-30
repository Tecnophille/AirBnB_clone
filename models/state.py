#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""State Module

This Module inherits from BaseModel class.
State Module contains the attributes to be assigned
to the States.
"""

from models.base_model import BaseModel


class State(BaseModel):
    """State Class

    Attributes:
        name (str): The State name

    """
    name = ''
