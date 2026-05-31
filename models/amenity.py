#!/usr/bin/python3
"""This module defines the Amenity class for the AirBnB clone project."""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Amenity class represents a feature or service offered by a place.

    Mapped to the 'amenities' table in DBStorage mode. Participates in a
    Many-to-Many relationship with Place via the place_amenity table.

    Attributes:
        __tablename__ (str): The MySQL table name.
        name (str): The name of the amenity.
    """

    __tablename__ = "amenities"

    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = relationship(
            "Place",
            secondary="place_amenity",
            viewonly=False
        )
