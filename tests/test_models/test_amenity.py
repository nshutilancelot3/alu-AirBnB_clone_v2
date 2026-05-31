#!/usr/bin/python3
"""Unit tests for the Amenity class."""
import os
import unittest
from models.amenity import Amenity
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):
    """Tests for the Amenity class attributes and methods."""

    def test_module_docstring(self):
        """Test that the amenity module has a docstring."""
        import models.amenity as a
        self.assertIsNotNone(a.__doc__)

    def test_class_docstring(self):
        """Test that the Amenity class has a docstring."""
        self.assertIsNotNone(Amenity.__doc__)

    def test_is_subclass_of_base_model(self):
        """Test that Amenity inherits from BaseModel."""
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)

    def test_instantiation(self):
        """Test Amenity can be instantiated."""
        amenity = Amenity()
        self.assertIsNotNone(amenity.id)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage attribute test only"
    )
    def test_name_is_class_attribute(self):
        """Test that name is a class attribute for FileStorage."""
        self.assertIn("name", Amenity.__dict__)

    def test_to_dict(self):
        """Test Amenity to_dict returns proper dictionary."""
        amenity = Amenity()
        amenity.name = "Pool"
        amenity_dict = amenity.to_dict()
        self.assertEqual(amenity_dict["__class__"], "Amenity")
        self.assertNotIn("_sa_instance_state", amenity_dict)

    def test_save(self):
        """Test that Amenity save() works."""
        amenity = Amenity()
        amenity.name = "Wifi"
        amenity.save()
        self.assertIsNotNone(amenity.updated_at)


if __name__ == "__main__":
    unittest.main()
