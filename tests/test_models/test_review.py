import unittest
from models.review import Review
from datetime import datetime
import uuid


class TestReview(unittest.TestCase):
    """
    Test cases for the Review class.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        self.review = Review()

    def test_instance_creation(self):
        """
        Test that an instance of Review is created.
        """
        self.assertIsInstance(self.review, Review)

    def test_attributes(self):
        """
        Test the attributes of the Review class.
        """
        self.assertTrue(hasattr(self.review, "id"))
        self.assertTrue(hasattr(self.review, "created_at"))
        self.assertTrue(hasattr(self.review, "updated_at"))
        self.assertTrue(hasattr(self.review, "place_id"))
        self.assertTrue(hasattr(self.review, "user_id"))
        self.assertTrue(hasattr(self.review, "text"))
        self.assertEqual(self.review.place_id, "")
        self.assertEqual(self.review.user_id, "")
        self.assertEqual(self.review.text, "")

    def test_id_is_uuid(self):
        """
        Test that id is a valid UUID.
        """
        self.assertIsInstance(uuid.UUID(self.review.id), uuid.UUID)

    def test_created_at_is_datetime(self):
        """
        Test that created_at is a datetime object.
        """
        self.assertIsInstance(self.review.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """
        Test that updated_at is a datetime object.
        """
        self.assertIsInstance(self.review.updated_at, datetime)

    def test_str_method(self):
        """
        Test the __str__ method.
        """
        string_rep = f"[Review] ({self.review.id}) {self.review.__dict__}"
        self.assertEqual(str(self.review), string_rep)

    def test_save_method(self):
        """
        Test the save method.
        """
        old_updated_at = self.review.updated_at
        self.review.save()
        self.assertNotEqual(self.review.updated_at, old_updated_at)

    def test_to_dict_method(self):
        """
        Test the to_dict method.
        """
        review_dict = self.review.to_dict()
        self.assertEqual(review_dict["__class__"], "Review")
        self.assertEqual(review_dict["id"], self.review.id)
        self.assertEqual(review_dict["created_at"],
                         self.review.created_at.isoformat())
        self.assertEqual(review_dict["updated_at"],
                         self.review.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
