#!/usr/bin/python3
"""Unit tests for the DBStorage class.

Tests verify DBStorage behavior with a live MySQL database using MySQLdb
for direct validation (isolated from the SQLAlchemy layer being tested).
"""
import os
import unittest


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") != "db",
    "DBStorage tests only"
)
class TestDBStorageInstantiation(unittest.TestCase):
    """Tests for DBStorage class attributes and docstrings."""

    def test_module_docstring(self):
        """Test that the db_storage module has a docstring."""
        import models.engine.db_storage as db_mod
        self.assertIsNotNone(db_mod.__doc__)
        self.assertGreater(len(db_mod.__doc__), 1)

    def test_class_docstring(self):
        """Test that the DBStorage class has a docstring."""
        from models.engine.db_storage import DBStorage
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertGreater(len(DBStorage.__doc__), 1)

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


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") != "db",
    "DBStorage tests only"
)
class TestDBStorageAll(unittest.TestCase):
    """Tests for DBStorage.all() method."""

    def setUp(self):
        """Import storage before each test."""
        from models import storage
        self.storage = storage

    def test_all_returns_dict(self):
        """Test that all() returns a dictionary."""
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    def test_all_with_state_class(self):
        """Test that all(State) returns only State objects."""
        from models.state import State
        result = self.storage.all(State)
        for obj in result.values():
            self.assertIsInstance(obj, State)

    def test_all_with_string_class_name(self):
        """Test that all('State') works as class filter."""
        result = self.storage.all("State")
        from models.state import State
        for obj in result.values():
            self.assertIsInstance(obj, State)

    def test_all_none_does_not_raise(self):
        """Test that all(None) returns a dict without raising."""
        result = self.storage.all(None)
        self.assertIsInstance(result, dict)

    def test_all_keys_format(self):
        """Test that all() keys follow ClassName.id format."""
        from models.state import State
        state = State(name="TestKeyFormat")
        state.save()
        result = self.storage.all(State)
        for key in result.keys():
            parts = key.split(".")
            self.assertEqual(len(parts), 2)
        self.storage.delete(state)
        self.storage.save()


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") != "db",
    "DBStorage tests only"
)
class TestDBStorageNewSave(unittest.TestCase):
    """Tests for DBStorage.new() and save() methods."""

    def setUp(self):
        """Import storage before each test."""
        from models import storage
        self.storage = storage

    def _db_connect(self):
        """Return a direct MySQLdb connection for isolation checks."""
        import MySQLdb
        return MySQLdb.connect(
            host=os.getenv("HBNB_MYSQL_HOST", "localhost"),
            user=os.getenv("HBNB_MYSQL_USER"),
            passwd=os.getenv("HBNB_MYSQL_PWD"),
            db=os.getenv("HBNB_MYSQL_DB")
        )

    def _count_table(self, table):
        """Return the current row count for a given table via direct SQL."""
        conn = self._db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM {}".format(table))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count

    def test_new_and_save_state_increments_db(self):
        """Test creating a State increases the states table count by 1."""
        from models.state import State
        before = self._count_table("states")
        state = State(name="DBTest_NewSave")
        state.save()
        after = self._count_table("states")
        self.assertEqual(after, before + 1)
        self.storage.delete(state)
        self.storage.save()

    def test_save_commits_to_db(self):
        """Test that save() actually persists data visible via direct SQL."""
        from models.state import State
        state = State(name="DBTest_Commit")
        state.save()
        conn = self._db_connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM states WHERE id = %s", (state.id,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "DBTest_Commit")
        self.storage.delete(state)
        self.storage.save()

    def test_new_adds_to_session(self):
        """Test that new() makes the object retrievable via all()."""
        from models.state import State
        state = State(name="DBTest_New")
        self.storage.new(state)
        self.storage.save()
        key = "State.{}".format(state.id)
        self.assertIn(key, self.storage.all(State))
        self.storage.delete(state)
        self.storage.save()


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") != "db",
    "DBStorage tests only"
)
class TestDBStorageDelete(unittest.TestCase):
    """Tests for DBStorage.delete() method."""

    def setUp(self):
        """Import storage before each test."""
        from models import storage
        self.storage = storage

    def _db_connect(self):
        """Return a direct MySQLdb connection for isolation checks."""
        import MySQLdb
        return MySQLdb.connect(
            host=os.getenv("HBNB_MYSQL_HOST", "localhost"),
            user=os.getenv("HBNB_MYSQL_USER"),
            passwd=os.getenv("HBNB_MYSQL_PWD"),
            db=os.getenv("HBNB_MYSQL_DB")
        )

    def test_delete_removes_from_db(self):
        """Test that delete() + save() decrements the states table count."""
        import MySQLdb
        from models.state import State
        state = State(name="DBTest_Delete")
        state.save()
        conn = self._db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        before = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.storage.delete(state)
        self.storage.save()
        conn = self._db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        after = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertEqual(after, before - 1)

    def test_delete_none_does_nothing(self):
        """Test that delete(None) does not raise or modify storage."""
        from models.state import State
        before = len(self.storage.all(State))
        self.storage.delete(None)
        after = len(self.storage.all(State))
        self.assertEqual(before, after)

    def test_delete_removes_from_all(self):
        """Test that deleted object no longer appears in all()."""
        from models.state import State
        state = State(name="DBTest_DeleteAll")
        state.save()
        key = "State.{}".format(state.id)
        self.assertIn(key, self.storage.all(State))
        self.storage.delete(state)
        self.storage.save()
        self.assertNotIn(key, self.storage.all(State))


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") != "db",
    "DBStorage tests only"
)
class TestDBStorageConsoleIntegration(unittest.TestCase):
    """Integration tests: verify console create commands hit the database."""

    def setUp(self):
        """Import storage before each test."""
        from models import storage
        self.storage = storage

    def _db_count(self, table):
        """Return row count for a table via direct MySQLdb connection."""
        import MySQLdb
        conn = MySQLdb.connect(
            host=os.getenv("HBNB_MYSQL_HOST", "localhost"),
            user=os.getenv("HBNB_MYSQL_USER"),
            passwd=os.getenv("HBNB_MYSQL_PWD"),
            db=os.getenv("HBNB_MYSQL_DB")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM {}".format(table))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count

    def test_console_create_state_increments_db(self):
        """Test that console 'create State' adds a record to the states table.

        Asserts a current DB state, runs the console command, then re-checks
        the DB directly with MySQLdb to confirm +1 record was added.
        """
        from io import StringIO
        from unittest.mock import patch
        from console import HBNBCommand
        before = self._db_count("states")
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd('create State name="ConsoleTestState"')
            obj_id = mock_out.getvalue().strip()
        after = self._db_count("states")
        self.assertEqual(after, before + 1)
        state = self.storage.all("State").get("State.{}".format(obj_id))
        if state:
            self.storage.delete(state)
            self.storage.save()

    def test_console_create_user_increments_db(self):
        """Test that console 'create User' adds a record to the users table."""
        from io import StringIO
        from unittest.mock import patch
        from console import HBNBCommand
        before = self._db_count("users")
        with patch("sys.stdout", new=StringIO()) as mock_out:
            HBNBCommand().onecmd(
                'create User email="test_db@test.com" password="pwd"'
            )
            obj_id = mock_out.getvalue().strip()
        after = self._db_count("users")
        self.assertEqual(after, before + 1)
        user = self.storage.all("User").get("User.{}".format(obj_id))
        if user:
            self.storage.delete(user)
            self.storage.save()


if __name__ == "__main__":
    unittest.main()
