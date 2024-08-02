import unittest
from models.user import User
from datetime import datetime
import uuid


class TestUser(unittest.TestCase):
    """
    Test cases for the User class.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        self.user = User()

    def test_instance_creation(self):
        """
        Test that an instance of User is created.
        """
        self.assertIsInstance(self.user, User)

    def test_attributes(self):
        """
        Test the attributes of the User class.
        """
        self.assertTrue(hasattr(self.user, "id"))
        self.assertTrue(hasattr(self.user, "created_at"))
        self.assertTrue(hasattr(self.user, "updated_at"))
        self.assertTrue(hasattr(self.user, "email"))
        self.assertTrue(hasattr(self.user, "password"))
        self.assertTrue(hasattr(self.user, "first_name"))
        self.assertTrue(hasattr(self.user, "last_name"))
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    def test_id_is_uuid(self):
        """
        Test that id is a valid UUID.
        """
        self.assertIsInstance(uuid.UUID(self.user.id), uuid.UUID)

    def test_created_at_is_datetime(self):
        """
        Test that created_at is a datetime object.
        """
        self.assertIsInstance(self.user.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """
        Test that updated_at is a datetime object.
        """
        self.assertIsInstance(self.user.updated_at, datetime)

    def test_str_method(self):
        """
        Test the __str__ method.
        """
        string_rep = f"[User] ({self.user.id}) {self.user.__dict__}"
        self.assertEqual(str(self.user), string_rep)

    def test_save_method(self):
        """
        Test the save method.
        """
        old_updated_at = self.user.updated_at
        self.user.save()
        self.assertNotEqual(self.user.updated_at, old_updated_at)

    def test_to_dict_method(self):
        """
        Test the to_dict method.
        """
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict["__class__"], "User")
        self.assertEqual(user_dict["id"], self.user.id)
        self.assertEqual(user_dict["created_at"],
                         self.user.created_at.isoformat())
        self.assertEqual(user_dict["updated_at"],
                         self.user.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
