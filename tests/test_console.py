#!/usr/bin/python3
"""Unit tests for the HBNBCommand console, focusing on do_create improvements.

Tests verify that the console correctly parses and applies typed key=value
parameters when creating objects with FileStorage.
"""
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place


class TestConsoleDoCreate(unittest.TestCase):
    """Tests for the updated do_create command with parameters."""

    def setUp(self):
        """Redirect stdout for capturing console output."""
        self.mock_stdout = StringIO()

    def tearDown(self):
        """Remove test objects from storage after each test."""
        self.mock_stdout.close()

    def test_module_docstring(self):
        """Test that the console module has a docstring."""
        import console as c
        self.assertIsNotNone(c.__doc__)

    def test_class_docstring(self):
        """Test that HBNBCommand has a docstring."""
        self.assertIsNotNone(HBNBCommand.__doc__)

    def test_do_create_docstring(self):
        """Test that do_create has a docstring."""
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)

    def test_create_no_class(self):
        """Test create with no class name prints error message."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd("create")
            self.assertIn("** class name missing **", mock_out.getvalue())

    def test_create_invalid_class(self):
        """Test create with unknown class name prints error message."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd("create NonExistent")
            self.assertIn("** class doesn't exist **", mock_out.getvalue())

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage tests only"
    )
    def test_create_state_with_name_param(self):
        """Test create State with string parameter sets name attribute."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd('create State name="California"')
            obj_id = mock_out.getvalue().strip()
        self.assertTrue(len(obj_id) > 0)
        key = "State.{}".format(obj_id)
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].name, "California")
        storage.delete(storage.all()[key])
        storage.save()

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage tests only"
    )
    def test_create_state_underscore_replaced_with_space(self):
        """Test that underscores in string params are replaced by spaces."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd('create State name="New_York"')
            obj_id = mock_out.getvalue().strip()
        key = "State.{}".format(obj_id)
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].name, "New York")
        storage.delete(storage.all()[key])
        storage.save()

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage tests only"
    )
    def test_create_place_with_integer_param(self):
        """Test create Place with an integer parameter."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd(
                'create Place city_id="0001" user_id="0001" '
                'name="Test" number_rooms=3'
            )
            obj_id = mock_out.getvalue().strip()
        key = "Place.{}".format(obj_id)
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].number_rooms, 3)
        storage.delete(storage.all()[key])
        storage.save()

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage tests only"
    )
    def test_create_place_with_float_param(self):
        """Test create Place with a float parameter."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd(
                'create Place city_id="0001" user_id="0001" '
                'name="Test" latitude=37.773972'
            )
            obj_id = mock_out.getvalue().strip()
        key = "Place.{}".format(obj_id)
        self.assertIn(key, storage.all())
        self.assertAlmostEqual(
            storage.all()[key].latitude, 37.773972, places=5
        )
        storage.delete(storage.all()[key])
        storage.save()

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage tests only"
    )
    def test_create_skips_invalid_params(self):
        """Test that invalid parameters are silently skipped."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd(
                'create State name="Valid" bad_param invalid=value'
            )
            obj_id = mock_out.getvalue().strip()
        key = "State.{}".format(obj_id)
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].name, "Valid")
        self.assertFalse(hasattr(storage.all()[key], "bad_param"))
        storage.delete(storage.all()[key])
        storage.save()

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage tests only"
    )
    def test_create_place_all_params(self):
        """Test create Place with all parameter types (string, int, float)."""
        cmd = (
            'create Place city_id="0001" user_id="0001" '
            'name="My_little_house" number_rooms=4 number_bathrooms=2 '
            'max_guest=10 price_by_night=300 '
            'latitude=37.773972 longitude=-122.431297'
        )
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd(cmd)
            obj_id = mock_out.getvalue().strip()
        key = "Place.{}".format(obj_id)
        self.assertIn(key, storage.all())
        place = storage.all()[key]
        self.assertEqual(place.name, "My little house")
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.max_guest, 10)
        self.assertAlmostEqual(place.latitude, 37.773972, places=5)
        self.assertAlmostEqual(place.longitude, -122.431297, places=5)
        storage.delete(place)
        storage.save()

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "DBStorage requires non-null name for State"
    )
    def test_create_returns_valid_id(self):
        """Test that create prints a valid UUID."""
        import uuid
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd('create State name="UUIDTest"')
            obj_id = mock_out.getvalue().strip()
        try:
            uuid.UUID(obj_id)
            valid = True
        except ValueError:
            valid = False
        self.assertTrue(valid)
        key = "State.{}".format(obj_id)
        if key in storage.all():
            storage.delete(storage.all()[key])
            storage.save()

    def test_create_returns_valid_id_db(self):
        """Test that create with required params prints a valid UUID."""
        import uuid
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd('create State name="UUIDTestDB"')
            obj_id = mock_out.getvalue().strip()
        try:
            uuid.UUID(obj_id)
            valid = True
        except ValueError:
            valid = False
        self.assertTrue(valid)
        key = "State.{}".format(obj_id)
        if key in storage.all():
            storage.delete(storage.all()[key])
            storage.save()

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage tests only"
    )
    def test_create_saves_to_storage(self):
        """Test that created object persists in storage."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd('create State name="Persist"')
            obj_id = mock_out.getvalue().strip()
        key = "State.{}".format(obj_id)
        self.assertIn(key, storage.all())
        storage.delete(storage.all()[key])
        storage.save()


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db",
    "FileStorage console tests only"
)
class TestConsoleAllCommand(unittest.TestCase):
    """Tests for the do_all command."""

    def test_all_no_class(self):
        """Test all command with no class returns list."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd("all")
            output = mock_out.getvalue().strip()
        self.assertTrue(output.startswith("["))

    def test_all_valid_class(self):
        """Test all command with valid class name."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd("all State")
            output = mock_out.getvalue().strip()
        self.assertTrue(output.startswith("["))

    def test_all_invalid_class(self):
        """Test all command with invalid class prints error."""
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd("all InvalidClass")
            output = mock_out.getvalue().strip()
        self.assertIn("** class doesn't exist **", output)


if __name__ == "__main__":
    unittest.main()
