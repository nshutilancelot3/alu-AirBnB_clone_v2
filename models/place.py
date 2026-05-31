#!/usr/bin/python3
"""This module defines the Place class for the AirBnB clone project."""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# Association table for the Many-to-Many relationship between Place and Amenity
place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False
    )
)


class Place(BaseModel, Base):
    """Place class represents a rental listing.

    Mapped to the 'places' table in DBStorage mode.

    Attributes:
        __tablename__ (str): The MySQL table name.
        city_id (str): Foreign key referencing cities.id.
        user_id (str): Foreign key referencing users.id.
        name (str): The name of the place.
        description (str): Description of the place (optional).
        number_rooms (int): Number of rooms (default 0).
        number_bathrooms (int): Number of bathrooms (default 0).
        max_guest (int): Maximum number of guests (default 0).
        price_by_night (int): Price per night (default 0).
        latitude (float): Latitude coordinate (optional).
        longitude (float): Longitude coordinate (optional).
    """

    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
            "Review",
            backref="place",
            cascade="all, delete-orphan"
        )
        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False
        )
    else:
        amenity_ids = []

        @property
        def reviews(self):
            """Return a list of Review instances with place_id == self.id.

            This is the FileStorage equivalent of the DBStorage relationship.
            """
            from models import storage
            from models.review import Review
            return [
                r for r in storage.all(Review).values()
                if r.place_id == self.id
            ]

        @property
        def amenities(self):
            """Return a list of Amenity instances linked to this place.

            Returns Amenity objects whose id is in self.amenity_ids.
            """
            from models import storage
            from models.amenity import Amenity
            return [
                a for a in storage.all(Amenity).values()
                if a.id in self.amenity_ids
            ]

        @amenities.setter
        def amenities(self, obj):
            """Append an Amenity's id to amenity_ids.

            Args:
                obj: An Amenity instance to link to this place.
            """
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
