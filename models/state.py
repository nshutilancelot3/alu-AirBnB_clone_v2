#!/usr/bin/python3
"""This module defines the State class for the AirBnB clone project."""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """State class represents a geographic state.

    For DBStorage: mapped to the 'states' table with SQLAlchemy ORM.
    For FileStorage: cities is a computed property returning related City objs.

    Attributes:
        __tablename__ (str): The MySQL table name.
        name (str): The name of the state.
    """

    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship(
            "City",
            backref="state",
            cascade="all, delete-orphan"
        )
    else:
        @property
        def cities(self):
            """Return a list of City instances with state_id == self.id.

            This is the FileStorage equivalent of the DBStorage relationship.
            """
            from models import storage
            from models.city import City
            return [
                city for city in storage.all(City).values()
                if city.state_id == self.id
            ]
