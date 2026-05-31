#!/usr/bin/python3
"""This module defines the City class for the AirBnB clone project."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """City class represents a city within a state.

    Mapped to the 'cities' table in DBStorage mode.

    Attributes:
        __tablename__ (str): The MySQL table name.
        state_id (str): Foreign key referencing states.id.
        name (str): The name of the city.
    """

    __tablename__ = "cities"

    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    name = Column(String(128), nullable=False)

    places = relationship(
        "Place",
        backref="cities",
        cascade="all, delete-orphan"
    )
