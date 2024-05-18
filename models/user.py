#!/usr/bin/python3
"""Defines the User class."""
from models.base_model import BaseModel


class User(BaseModel):
    """Represent a User.

    Attributes:
        email (str): The email
        password (str): The password
        first_name (str): The first name
        last_name (str): The last name
    """
    first_name = ""
    last_name = ""
    email = ""
    password = ""
