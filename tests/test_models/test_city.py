#!/usr/bin/python3
"""Unit tests for the City class."""
import os
import unittest
from models.city import City
from models.base_model import BaseModel


class TestCity(unittest.TestCase):
    """Tests for the City class attributes and methods."""

    def test_module_docstring(self):
        """Test that the city module has a docstring."""
        import models.city as c
        self.assertIsNotNone(c.__doc__)

    def test_class_docstring(self):
        """Test that the City class has a docstring."""
        self.assertIsNotNone(City.__doc__)

    def test_is_subclass_of_base_model(self):
        """Test that City inherits from BaseModel."""
        city = City()
        self.assertIsInstance(city, BaseModel)

    def test_instantiation(self):
        """Test City can be instantiated."""
        city = City()
        self.assertIsNotNone(city.id)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage attribute test only"
    )
    def test_class_attributes(self):
        """Test that state_id and name are class attributes in FileStorage."""
        self.assertIn("state_id", City.__dict__)
        self.assertIn("name", City.__dict__)

    def test_to_dict(self):
        """Test City to_dict does not contain _sa_instance_state."""
        city = City()
        city_dict = city.to_dict()
        self.assertNotIn("_sa_instance_state", city_dict)
        self.assertEqual(city_dict["__class__"], "City")


if __name__ == "__main__":
    unittest.main()
