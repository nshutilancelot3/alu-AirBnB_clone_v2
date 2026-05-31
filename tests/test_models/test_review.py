#!/usr/bin/python3
"""Unit tests for the Review class."""
import os
import unittest
from models.review import Review
from models.base_model import BaseModel


class TestReview(unittest.TestCase):
    """Tests for the Review class attributes and methods."""

    def test_module_docstring(self):
        """Test that the review module has a docstring."""
        import models.review as r
        self.assertIsNotNone(r.__doc__)

    def test_class_docstring(self):
        """Test that the Review class has a docstring."""
        self.assertIsNotNone(Review.__doc__)

    def test_is_subclass_of_base_model(self):
        """Test that Review inherits from BaseModel."""
        review = Review()
        self.assertIsInstance(review, BaseModel)

    def test_instantiation(self):
        """Test Review can be instantiated."""
        review = Review()
        self.assertIsNotNone(review.id)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "FileStorage attribute test only"
    )
    def test_class_attributes_file_storage(self):
        """Test Review class attributes for FileStorage mode."""
        self.assertIn("place_id", Review.__dict__)
        self.assertIn("user_id", Review.__dict__)
        self.assertIn("text", Review.__dict__)

    def test_to_dict(self):
        """Test Review to_dict returns proper dictionary."""
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(review_dict["__class__"], "Review")
        self.assertNotIn("_sa_instance_state", review_dict)


if __name__ == "__main__":
    unittest.main()
