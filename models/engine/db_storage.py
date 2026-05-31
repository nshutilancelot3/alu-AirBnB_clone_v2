#!/usr/bin/python3
"""This module defines the DBStorage class for the AirBnB clone project.

DBStorage uses SQLAlchemy to map model classes to a MySQL database,
replacing the JSON-based FileStorage when HBNB_TYPE_STORAGE=db.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """DBStorage manages a MySQL database session via SQLAlchemy.

    Private class attributes:
        __engine: SQLAlchemy engine instance.
        __session: SQLAlchemy scoped session instance.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance.

        Creates a SQLAlchemy engine connected to the MySQL database
        specified by HBNB_MYSQL_* environment variables. If HBNB_ENV
        equals 'test', all tables are dropped before use.
        """
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST", "localhost")
        db = os.getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db),
            pool_pre_ping=True
        )

        if os.getenv("HBNB_ENV") == "test":
            from models.base_model import Base
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of a given class from the current session.

        Args:
            cls (class or str, optional): The class to query. If None,
                queries all supported model classes.

        Returns:
            dict: A dictionary keyed by <ClassName>.<id> mapping to objects.
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
        }

        result = {}
        if cls is not None:
            if isinstance(cls, str):
                cls = classes.get(cls, None)
            if cls is not None:
                for obj in self.__session.query(cls).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    result[key] = obj
        else:
            for c in classes.values():
                for obj in self.__session.query(c).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    result[key] = obj
        return result

    def new(self, obj):
        """Add an object to the current database session.

        Args:
            obj: The model instance to add.
        """
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session.

        Args:
            obj: The model instance to delete. If None, does nothing.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and initialize the scoped session.

        Imports all model classes to ensure they are registered with
        SQLAlchemy's metadata before creating tables.
        """
        from models.base_model import Base
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the current session."""
        self.__session.close()
