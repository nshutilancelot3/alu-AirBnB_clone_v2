#!/usr/bin/python3
"""This module defines the User class for the AirBnB clone project."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """User class represents an application user.

    Mapped to the 'users' table in DBStorage mode.

    Attributes:
        __tablename__ (str): The MySQL table name.
        email (str): The email address of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user (optional).
        last_name (str): The last name of the user (optional).
    """

    __tablename__ = "users"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    places = relationship(
        "Place",
        backref="user",
        cascade="all, delete-orphan"
    )
    reviews = relationship(
        "Review",
        backref="user",
        cascade="all, delete-orphan"
    )
