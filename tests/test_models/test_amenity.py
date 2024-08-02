import unittest
from models.amenity import Amenity
from datetime import datetime
import uuid


class TestAmenity(unittest.TestCase):
    """
    Test cases for the Amenity class.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        self.amenity = Amenity()

    def test_instance_creation(self):
        """
        Test that an instance of Amenity is created.
        """
        self.assertIsInstance(self.amenity, Amenity)

    def test_attributes(self):
        """
        Test the attributes of the Amenity class.
        """
        self.assertTrue(hasattr(self.amenity, "id"))
        self.assertTrue(hasattr(self.amenity, "created_at"))
        self.assertTrue(hasattr(self.amenity, "updated_at"))
        self.assertTrue(hasattr(self.amenity, "name"))
        self.assertEqual(self.amenity.name, "")

    def test_id_is_uuid(self):
        """
        Test that id is a valid UUID.
        """
        self.assertIsInstance(uuid.UUID(self.amenity.id), uuid.UUID)

    def test_created_at_is_datetime(self):
        """
        Test that created_at is a datetime object.
        """
        self.assertIsInstance(self.amenity.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """
        Test that updated_at is a datetime object.
        """
        self.assertIsInstance(self.amenity.updated_at, datetime)

    def test_str_method(self):
        """
        Test the __str__ method.
        """
        string_rep = f"[Amenity] ({self.amenity.id}) {self.amenity.__dict__}"
        self.assertEqual(str(self.amenity), string_rep)

    def test_save_method(self):
        """
        Test the save method.
        """
        old_updated_at = self.amenity.updated_at
        self.amenity.save()
        self.assertNotEqual(self.amenity.updated_at, old_updated_at)

    def test_to_dict_method(self):
        """
        Test the to_dict method.
        """
        amenity_dict = self.amenity.to_dict()
        self.assertEqual(amenity_dict["__class__"], "Amenity")
        self.assertEqual(amenity_dict["id"], self.amenity.id)
        self.assertEqual(amenity_dict["created_at"],
                         self.amenity.created_at.isoformat())
        self.assertEqual(amenity_dict["updated_at"],
                         self.amenity.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
