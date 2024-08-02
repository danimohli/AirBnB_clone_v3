import unittest
from models.city import City
from datetime import datetime
import uuid


class TestCity(unittest.TestCase):
    """
    Test cases for the City class.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        self.city = City()

    def test_instance_creation(self):
        """
        Test that an instance of City is created.
        """
        self.assertIsInstance(self.city, City)

    def test_attributes(self):
        """
        Test the attributes of the City class.
        """
        self.assertTrue(hasattr(self.city, "id"))
        self.assertTrue(hasattr(self.city, "created_at"))
        self.assertTrue(hasattr(self.city, "updated_at"))
        self.assertTrue(hasattr(self.city, "name"))
        self.assertTrue(hasattr(self.city, "state_id"))
        self.assertEqual(self.city.name, "")
        self.assertEqual(self.city.state_id, "")

    def test_id_is_uuid(self):
        """
        Test that id is a valid UUID.
        """
        self.assertIsInstance(uuid.UUID(self.city.id), uuid.UUID)

    def test_created_at_is_datetime(self):
        """
        Test that created_at is a datetime object.
        """
        self.assertIsInstance(self.city.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """
        Test that updated_at is a datetime object.
        """
        self.assertIsInstance(self.city.updated_at, datetime)

    def test_str_method(self):
        """
        Test the __str__ method.
        """
        string_rep = f"[City] ({self.city.id}) {self.city.__dict__}"
        self.assertEqual(str(self.city), string_rep)

    def test_save_method(self):
        """
        Test the save method.
        """
        old_updated_at = self.city.updated_at
        self.city.save()
        self.assertNotEqual(self.city.updated_at, old_updated_at)

    def test_to_dict_method(self):
        """
        Test the to_dict method.
        """
        city_dict = self.city.to_dict()
        self.assertEqual(city_dict["__class__"], "City")
        self.assertEqual(city_dict["id"], self.city.id)
        self.assertEqual(city_dict["created_at"],
                         self.city.created_at.isoformat())
        self.assertEqual(city_dict["updated_at"],
                         self.city.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
