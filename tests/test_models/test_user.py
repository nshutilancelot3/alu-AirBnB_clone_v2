#!/usr/bin/python3
"""Unit tests for the User class."""
import os
import unittest
from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """Tests for the User class attributes and methods."""

    def test_module_docstring(self):
        """Test that the user module has a docstring."""
        import models.user as u
        self.assertIsNotNone(u.__doc__)

    def test_class_docstring(self):
        """Test that the User class has a docstring."""
        self.assertIsNotNone(User.__doc__)

    def test_is_subclass_of_base_model(self):
        """Test that User inherits from BaseModel."""
        user = User()
        self.assertIsInstance(user, BaseModel)

    def test_instantiation(self):
        """Test User can be instantiated."""
        user = User()
        self.assertIsNotNone(user.id)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage attribute test only"
    )
    def test_class_attributes_file_storage(self):
        """Test User class attributes exist for FileStorage."""
        self.assertIn("email", User.__dict__)
        self.assertIn("password", User.__dict__)
        self.assertIn("first_name", User.__dict__)
        self.assertIn("last_name", User.__dict__)

    def test_to_dict(self):
        """Test User to_dict returns proper dictionary."""
        user = User()
        user_dict = user.to_dict()
        self.assertEqual(user_dict["__class__"], "User")
        self.assertNotIn("_sa_instance_state", user_dict)

    def test_save(self):
        """Test that User save() works."""
        user = User()
        user.email = "test@example.com"
        user.password = "testpass"
        user.save()
        self.assertIsNotNone(user.updated_at)


if __name__ == "__main__":
    unittest.main()
