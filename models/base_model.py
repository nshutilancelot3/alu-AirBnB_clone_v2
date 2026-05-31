#!/usr/bin/python3
"""This module defines the BaseModel class for the AirBnB clone project.

BaseModel provides common attributes (id, created_at, updated_at) and
methods (save, to_dict, delete) shared by all model classes. It also
declares the SQLAlchemy declarative Base used by DBStorage models.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """BaseModel defines all common attributes and methods for other classes.

    When used with DBStorage, subclasses inherit from both BaseModel and Base
    to gain SQLAlchemy ORM mapping.

    Attributes:
        id (str): Unique string identifier (UUID), primary key (60 chars).
        created_at (datetime): Datetime when the instance was created.
        updated_at (datetime): Datetime when the instance was last updated.
    """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance.

        Args:
            *args: Unused positional arguments.
            **kwargs: Key/value pairs to set as instance attributes.
                      If provided, creates an instance from a dictionary.
                      Otherwise, generates a new unique id and timestamps.
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in ("created_at", "updated_at"):
                    if isinstance(value, str):
                        value = datetime.strptime(value, time_format)
                setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """Return a human-readable string representation of the instance."""
        d = {k: v for k, v in self.__dict__.items()
             if k != "_sa_instance_state"}
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)

    def save(self):
        """Update updated_at with the current datetime and persist to storage.

        For DBStorage, the object is added to the session before saving.
        """
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance.

        Returns:
            dict: A dictionary containing all instance attributes,
                  with created_at and updated_at as ISO format strings,
                  a __class__ key with the class name, and without
                  the SQLAlchemy _sa_instance_state key.
        """
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = type(self).__name__
        if isinstance(obj_dict.get("created_at"), datetime):
            obj_dict["created_at"] = obj_dict["created_at"].isoformat()
        if isinstance(obj_dict.get("updated_at"), datetime):
            obj_dict["updated_at"] = obj_dict["updated_at"].isoformat()
        obj_dict.pop("_sa_instance_state", None)
        return obj_dict

    def delete(self):
        """Delete the current instance from storage."""
        from models import storage
        storage.delete(self)
