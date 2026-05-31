#!/usr/bin/python3
"""This module defines the Review class for the AirBnB clone project."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Review class represents a user review for a rental place.

    Mapped to the 'reviews' table in DBStorage mode.

    Attributes:
        __tablename__ (str): The MySQL table name.
        text (str): The content of the review.
        place_id (str): Foreign key referencing places.id.
        user_id (str): Foreign key referencing users.id.
    """

    __tablename__ = "reviews"

    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
