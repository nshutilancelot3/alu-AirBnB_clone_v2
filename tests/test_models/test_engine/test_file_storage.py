#!/usr/bin/python3
"""Unit tests for the FileStorage class."""
import os
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db",
    "FileStorage tests only"
)
class TestFileStorage(unittest.TestCase):
    """Tests for the FileStorage class."""

    def setUp(self):
        """Set up a fresh FileStorage instance for each test."""
        self.storage = FileStorage()

    def test_module_docstring(self):
        """Test that the module has a docstring."""
        import models.engine.file_storage as fs_mod
        self.assertIsNotNone(fs_mod.__doc__)

    def test_class_docstring(self):
        """Test that the FileStorage class has a docstring."""
        self.assertIsNotNone(FileStorage.__doc__)

    def test_all_returns_dict(self):
        """Test that all() returns a dictionary."""
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    def test_all_no_class_filter(self):
        """Test that all() without argument returns all objects."""
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    def test_all_with_class_filter(self):
        """Test that all(cls) returns only objects of that class."""
        state = State()
        state.name = "TestState"
        self.storage.new(state)
        result = self.storage.all(State)
        for key, obj in result.items():
            self.assertIsInstance(obj, State)

    def test_all_with_string_class_filter(self):
        """Test that all('ClassName') works as a filter."""
        state = State()
        state.name = "AnotherTestState"
        self.storage.new(state)
        result = self.storage.all("State")
        for key, obj in result.items():
            self.assertIsInstance(obj, State)

    def test_new_adds_object(self):
        """Test that new() adds an object to __objects."""
        obj = BaseModel()
        self.storage.new(obj)
        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, self.storage.all())

    def test_delete_removes_object(self):
        """Test that delete() removes an object from __objects."""
        obj = BaseModel()
        self.storage.new(obj)
        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, self.storage.all())
        self.storage.delete(obj)
        self.assertNotIn(key, self.storage.all())

    def test_delete_none_does_nothing(self):
        """Test that delete(None) does not raise or modify storage."""
        count_before = len(self.storage.all())
        self.storage.delete(None)
        count_after = len(self.storage.all())
        self.assertEqual(count_before, count_after)

    def test_save_and_reload(self):
        """Test that save() and reload() persist and restore objects."""
        obj = State()
        obj.name = "PersistState"
        self.storage.new(obj)
        self.storage.save()

        new_storage = FileStorage()
        new_storage.reload()
        key = "State.{}".format(obj.id)
        self.assertIn(key, new_storage.all())

    def test_all_filters_correctly(self):
        """Test that filtering by class excludes other class objects."""
        user = User()
        user.email = "test@test.com"
        user.password = "pass"
        state = State()
        state.name = "FilterState"
        self.storage.new(user)
        self.storage.new(state)
        states = self.storage.all(State)
        for obj in states.values():
            self.assertNotIsInstance(obj, User)


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db",
    "FileStorage tests only"
)
class TestFileStorageDocstrings(unittest.TestCase):
    """Test docstrings in FileStorage methods."""

    def test_all_docstring(self):
        """Test that all() method has a docstring."""
        self.assertIsNotNone(FileStorage.all.__doc__)

    def test_new_docstring(self):
        """Test that new() method has a docstring."""
        self.assertIsNotNone(FileStorage.new.__doc__)

    def test_save_docstring(self):
        """Test that save() method has a docstring."""
        self.assertIsNotNone(FileStorage.save.__doc__)

    def test_reload_docstring(self):
        """Test that reload() method has a docstring."""
        self.assertIsNotNone(FileStorage.reload.__doc__)

    def test_delete_docstring(self):
        """Test that delete() method has a docstring."""
        self.assertIsNotNone(FileStorage.delete.__doc__)


if __name__ == "__main__":
    unittest.main()
