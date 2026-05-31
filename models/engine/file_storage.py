#!/usr/bin/python3
"""This module defines the FileStorage class for the AirBnB clone project."""
import json


class FileStorage:
    """FileStorage serializes instances to a JSON file and deserializes back.

    Attributes:
        __file_path (str): Path to the JSON file.
        __objects (dict): Dictionary storing all objects by <class name>.id.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return the dictionary of all stored objects, optionally filtered.

        Args:
            cls (class or str, optional): If provided, return only objects
                that are instances of this class. Defaults to None.

        Returns:
            dict: A dictionary of objects keyed by <ClassName>.<id>.
        """
        if cls is None:
            return FileStorage.__objects
        result = {}
        for key, obj in FileStorage.__objects.items():
            if isinstance(cls, str):
                if type(obj).__name__ == cls:
                    result[key] = obj
            else:
                if isinstance(obj, cls):
                    result[key] = obj
        return result

    def new(self, obj):
        """Set obj in __objects with key <obj class name>.id.

        Args:
            obj: An instance of a model class.
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file at __file_path."""
        json_objects = {}
        for key, obj in FileStorage.__objects.items():
            json_objects[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserialize the JSON file to __objects if the file exists.

        If the file does not exist, no exception is raised.
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

        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                json_objects = json.load(f)
            for key, value in json_objects.items():
                class_name = value.get("__class__")
                if class_name in classes:
                    FileStorage.__objects[key] = classes[class_name](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it exists.

        Args:
            obj: The object to delete. If None, does nothing.
        """
        if obj is None:
            return
        key = "{}.{}".format(type(obj).__name__, obj.id)
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]

    def close(self):
        """Call reload to deserialize the JSON file to objects."""
        self.reload()
