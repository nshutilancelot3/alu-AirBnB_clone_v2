#!/usr/bin/python3
"""Unit tests for the Place class."""
import os
import unittest
from models.place import Place
from models.base_model import BaseModel


class TestPlace(unittest.TestCase):
    """Tests for the Place class attributes and methods."""

    def test_module_docstring(self):
        """Test that the place module has a docstring."""
        import models.place as p
        self.assertIsNotNone(p.__doc__)

    def test_class_docstring(self):
        """Test that the Place class has a docstring."""
        self.assertIsNotNone(Place.__doc__)

    def test_is_subclass_of_base_model(self):
        """Test that Place inherits from BaseModel."""
        place = Place()
        self.assertIsInstance(place, BaseModel)

    def test_instantiation(self):
        """Test Place can be instantiated."""
        place = Place()
        self.assertIsNotNone(place.id)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage attribute test only"
    )
    def test_class_attributes_file_storage(self):
        """Test Place class attributes for FileStorage mode."""
        self.assertIn("city_id", Place.__dict__)
        self.assertIn("user_id", Place.__dict__)
        self.assertIn("name", Place.__dict__)
        self.assertIn("number_rooms", Place.__dict__)
        self.assertIn("number_bathrooms", Place.__dict__)
        self.assertIn("max_guest", Place.__dict__)
        self.assertIn("price_by_night", Place.__dict__)
        self.assertIn("latitude", Place.__dict__)
        self.assertIn("longitude", Place.__dict__)

    def test_to_dict(self):
        """Test Place to_dict returns proper dictionary."""
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(place_dict["__class__"], "Place")
        self.assertNotIn("_sa_instance_state", place_dict)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage amenities property test only"
    )
    def test_amenities_getter(self):
        """Test the amenities getter returns a list for FileStorage."""
        place = Place()
        amenities = place.amenities
        self.assertIsInstance(amenities, list)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage amenities setter test only"
    )
    def test_amenities_setter(self):
        """Test the amenities setter appends amenity id for FileStorage."""
        from models.amenity import Amenity
        place = Place()
        amenity = Amenity()
        amenity.name = "Wifi"
        place.amenities = amenity
        self.assertIn(amenity.id, place.amenity_ids)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage reviews property test only"
    )
    def test_reviews_getter(self):
        """Test the reviews getter returns a list for FileStorage."""
        place = Place()
        reviews = place.reviews
        self.assertIsInstance(reviews, list)


if __name__ == "__main__":
    unittest.main()
