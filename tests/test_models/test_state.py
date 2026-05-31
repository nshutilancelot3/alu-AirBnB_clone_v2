#!/usr/bin/python3
"""Unit tests for the State class."""
import os
import unittest
from models.state import State
from models.base_model import BaseModel


class TestState(unittest.TestCase):
    """Tests for the State class attributes and methods."""

    def test_module_docstring(self):
        """Test that the state module has a docstring."""
        import models.state as s
        self.assertIsNotNone(s.__doc__)

    def test_class_docstring(self):
        """Test that the State class has a docstring."""
        self.assertIsNotNone(State.__doc__)

    def test_is_subclass_of_base_model(self):
        """Test that State inherits from BaseModel."""
        state = State()
        self.assertIsInstance(state, BaseModel)

    def test_instantiation(self):
        """Test State can be instantiated."""
        state = State()
        self.assertIsNotNone(state.id)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage attribute test only"
    )
    def test_name_is_class_attribute(self):
        """Test that name is a class attribute for FileStorage."""
        self.assertIn("name", State.__dict__)

    def test_save_and_to_dict(self):
        """Test State save and to_dict methods."""
        state = State()
        state.name = "TestState"
        state.save()
        state_dict = state.to_dict()
        self.assertEqual(state_dict["__class__"], "State")
        self.assertNotIn("_sa_instance_state", state_dict)


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db",
    "FileStorage tests only"
)
class TestStateFileStorage(unittest.TestCase):
    """Tests for State with FileStorage."""

    def test_cities_property(self):
        """Test that cities property returns related City instances."""
        from models.city import City
        from models import storage
        state = State()
        state.name = "California"
        state.save()

        city = City()
        city.state_id = state.id
        city.name = "San Francisco"
        city.save()

        cities = state.cities
        self.assertIsInstance(cities, list)
        self.assertTrue(any(c.id == city.id for c in cities))

        # Clean up
        storage.delete(state)
        storage.delete(city)
        storage.save()


if __name__ == "__main__":
    unittest.main()
