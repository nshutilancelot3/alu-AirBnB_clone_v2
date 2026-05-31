#!/usr/bin/python3
"""This module instantiates the appropriate storage object.

Depending on the HBNB_TYPE_STORAGE environment variable:
    - 'db': uses DBStorage (MySQL via SQLAlchemy)
    - anything else (default): uses FileStorage (JSON file)
"""
import os

storage_type = os.getenv("HBNB_TYPE_STORAGE")

if storage_type == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
