#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents the BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        tform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())  # Unique identifier for each instance
        self.created_at = datetime.today()  # Date and time of instance creation
        self.updated_at = datetime.today()  # Date and time of instance update
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    self.__dict__[key] = datetime.strptime(value, tform)  # Convert string to datetime
                else:
                    self.__dict__[key] = value  # Set attribute dynamically
        else:
            models.storage.new(self)  # Add instance to storage

    def save(self):
        """Update updated_at with the current datetime and save the instance."""
        self.updated_at = datetime.today()  # Update the update time to current datetime
        models.storage.save()  # Save the instance

    def to_dict(self):
        """Return the dictionary representation of the BaseModel instance.

        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        rdict = self.__dict__.copy()  # Create a copy of the instance's attributes
        rdict["created_at"] = self.created_at.isoformat()  # Format datetime as string
        rdict["updated_at"] = self.updated_at.isoformat()  # Format datetime as string
        rdict["__class__"] = self.__class__.__name__  # Add class name to the dictionary
        return rdict

    def __str__(self):
        """Return the string representation of the BaseModel instance."""
        clname = self.__class__.__name__  # Get the name of the class
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)  # Format the string representation