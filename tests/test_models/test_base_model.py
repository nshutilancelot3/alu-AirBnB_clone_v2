#!/usr/bin/python3
"""Unit tests for the BaseModel class."""
import os
import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Tests for the BaseModel class attributes and methods."""

    def test_module_docstring(self):
        """Test that the module has a docstring."""
        import models.base_model as bm
        self.assertIsNotNone(bm.__doc__)

    def test_class_docstring(self):
        """Test that the BaseModel class has a docstring."""
        self.assertIsNotNone(BaseModel.__doc__)

    def test_init_no_args(self):
        """Test BaseModel instantiation with no arguments."""
        obj = BaseModel()
        self.assertIsInstance(obj.id, str)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)

    def test_unique_ids(self):
        """Test that two BaseModel instances have different ids."""
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.assertNotEqual(obj1.id, obj2.id)

    def test_init_with_kwargs(self):
        """Test BaseModel instantiation with keyword arguments."""
        data = {
            "id": "test-id-123",
            "created_at": "2024-01-01T00:00:00.000000",
            "updated_at": "2024-01-01T00:00:00.000000",
            "name": "Test"
        }
        obj = BaseModel(**data)
        self.assertEqual(obj.id, "test-id-123")
        self.assertEqual(obj.name, "Test")
        self.assertIsInstance(obj.created_at, datetime)

    def test_to_dict(self):
        """Test the to_dict method returns proper dictionary."""
        obj = BaseModel()
        obj_dict = obj.to_dict()
        self.assertIn("__class__", obj_dict)
        self.assertEqual(obj_dict["__class__"], "BaseModel")
        self.assertIsInstance(obj_dict["created_at"], str)
        self.assertIsInstance(obj_dict["updated_at"], str)
        self.assertNotIn("_sa_instance_state", obj_dict)

    def test_str_representation(self):
        """Test the __str__ method returns correct format."""
        obj = BaseModel()
        expected = "[BaseModel] ({}) {}".format(obj.id, obj.__dict__)
        self.assertEqual(str(obj), expected)

    def test_save_updates_updated_at(self):
        """Test that save() updates the updated_at attribute."""
        obj = BaseModel()
        old_updated_at = obj.updated_at
        obj.save()
        self.assertGreaterEqual(obj.updated_at, old_updated_at)

    def test_kwargs_ignores_class_key(self):
        """Test that __class__ key in kwargs is ignored."""
        data = {
            "__class__": "SomeClass",
            "id": "some-id",
            "created_at": "2024-01-01T00:00:00.000000",
            "updated_at": "2024-01-01T00:00:00.000000"
        }
        obj = BaseModel(**data)
        self.assertEqual(type(obj).__name__, "BaseModel")


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db",
    "FileStorage tests only"
)
class TestBaseModelFileStorage(unittest.TestCase):
    """Tests for BaseModel specifically with FileStorage."""

    def test_save_persists_to_storage(self):
        """Test that save() stores the object in FileStorage."""
        from models import storage
        obj = BaseModel()
        obj.save()
        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, storage.all())


if __name__ == "__main__":
    unittest.main()
