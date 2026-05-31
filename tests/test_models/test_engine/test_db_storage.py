#!/usr/bin/python3
"""Unit tests for the DBStorage class."""
import os
import unittest


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") != "db",
    "DBStorage tests only"
)
class TestDBStorage(unittest.TestCase):
    """Tests for the DBStorage class using MySQL."""

    def setUp(self):
        """Import storage for each test."""
        from models import storage
        self.storage = storage

    def test_module_docstring(self):
        """Test that the db_storage module has a docstring."""
        import models.engine.db_storage as db_mod
        self.assertIsNotNone(db_mod.__doc__)

    def test_class_docstring(self):
        """Test that the DBStorage class has a docstring."""
        from models.engine.db_storage import DBStorage
        self.assertIsNotNone(DBStorage.__doc__)

    def test_all_returns_dict(self):
        """Test that all() returns a dictionary."""
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    def test_all_with_class_filter(self):
        """Test that all(State) returns only State objects."""
        from models.state import State
        result = self.storage.all(State)
        for obj in result.values():
            self.assertIsInstance(obj, State)

    def test_new_and_save_state(self):
        """Test creating a State is reflected in all()."""
        import MySQLdb
        from models.state import State

        # Count states before
        db_conn = MySQLdb.connect(
            host=os.getenv("HBNB_MYSQL_HOST", "localhost"),
            user=os.getenv("HBNB_MYSQL_USER"),
            passwd=os.getenv("HBNB_MYSQL_PWD"),
            db=os.getenv("HBNB_MYSQL_DB")
        )
        cursor = db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        count_before = cursor.fetchone()[0]
        cursor.close()
        db_conn.close()

        # Create and save a new State
        state = State(name="TestState_DBStorage")
        state.save()

        # Count states after
        db_conn = MySQLdb.connect(
            host=os.getenv("HBNB_MYSQL_HOST", "localhost"),
            user=os.getenv("HBNB_MYSQL_USER"),
            passwd=os.getenv("HBNB_MYSQL_PWD"),
            db=os.getenv("HBNB_MYSQL_DB")
        )
        cursor = db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        count_after = cursor.fetchone()[0]
        cursor.close()
        db_conn.close()

        self.assertEqual(count_after, count_before + 1)

        # Clean up
        self.storage.delete(state)
        self.storage.save()

    def test_delete_state(self):
        """Test that deleting a State removes it from the database."""
        import MySQLdb
        from models.state import State

        # Create a state to delete
        state = State(name="DeleteMe_DBStorage")
        state.save()

        # Count before deletion
        db_conn = MySQLdb.connect(
            host=os.getenv("HBNB_MYSQL_HOST", "localhost"),
            user=os.getenv("HBNB_MYSQL_USER"),
            passwd=os.getenv("HBNB_MYSQL_PWD"),
            db=os.getenv("HBNB_MYSQL_DB")
        )
        cursor = db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        count_before = cursor.fetchone()[0]
        cursor.close()
        db_conn.close()

        self.storage.delete(state)
        self.storage.save()

        # Count after deletion
        db_conn = MySQLdb.connect(
            host=os.getenv("HBNB_MYSQL_HOST", "localhost"),
            user=os.getenv("HBNB_MYSQL_USER"),
            passwd=os.getenv("HBNB_MYSQL_PWD"),
            db=os.getenv("HBNB_MYSQL_DB")
        )
        cursor = db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        count_after = cursor.fetchone()[0]
        cursor.close()
        db_conn.close()

        self.assertEqual(count_after, count_before - 1)

    def test_all_docstring(self):
        """Test that all() method has a docstring."""
        from models.engine.db_storage import DBStorage
        self.assertIsNotNone(DBStorage.all.__doc__)

    def test_new_docstring(self):
        """Test that new() method has a docstring."""
        from models.engine.db_storage import DBStorage
        self.assertIsNotNone(DBStorage.new.__doc__)

    def test_save_docstring(self):
        """Test that save() method has a docstring."""
        from models.engine.db_storage import DBStorage
        self.assertIsNotNone(DBStorage.save.__doc__)

    def test_delete_docstring(self):
        """Test that delete() method has a docstring."""
        from models.engine.db_storage import DBStorage
        self.assertIsNotNone(DBStorage.delete.__doc__)

    def test_reload_docstring(self):
        """Test that reload() method has a docstring."""
        from models.engine.db_storage import DBStorage
        self.assertIsNotNone(DBStorage.reload.__doc__)


if __name__ == "__main__":
    unittest.main()
