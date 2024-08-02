import unittest
from models.place import Place
from datetime import datetime
import uuid


class TestPlace(unittest.TestCase):
    """
    Test cases for the Place class.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        self.place = Place()

    def test_instance_creation(self):
        """
        Test that an instance of Place is created.
        """
        self.assertIsInstance(self.place, Place)

    def test_attributes(self):
        """
        Test the attributes of the Place class.
        """

        self.assertTrue(hasattr(self.place, "id"))
        self.assertTrue(hasattr(self.place, "created_at"))
        self.assertTrue(hasattr(self.place, "updated_at"))
        self.assertTrue(hasattr(self.place, "city_id"))
        self.assertTrue(hasattr(self.place, "user_id"))
        self.assertTrue(hasattr(self.place, "name"))
        self.assertTrue(hasattr(self.place, "description"))
        self.assertTrue(hasattr(self.place, "number_rooms"))
        self.assertTrue(hasattr(self.place, "number_bathrooms"))
        self.assertTrue(hasattr(self.place, "max_guest"))
        self.assertTrue(hasattr(self.place, "price_by_night"))
        self.assertTrue(hasattr(self.place, "latitude"))
        self.assertTrue(hasattr(self.place, "longitude"))
        self.assertTrue(hasattr(self.place, "amenity_ids"))
        self.assertEqual(self.place.city_id, "")
        self.assertEqual(self.place.user_id, "")
        self.assertEqual(self.place.name, "")
        self.assertEqual(self.place.description, "")
        self.assertEqual(self.place.number_rooms, 0)
        self.assertEqual(self.place.number_bathrooms, 0)
        self.assertEqual(self.place.max_guest, 0)
        self.assertEqual(self.place.price_by_night, 0)
        self.assertEqual(self.place.latitude, 0.0)
        self.assertEqual(self.place.longitude, 0.0)
        self.assertEqual(self.place.amenity_ids, [])

    def test_id_is_uuid(self):
        """
        Test that id is a valid UUID.
        """
        self.assertIsInstance(uuid.UUID(self.place.id), uuid.UUID)

    def test_created_at_is_datetime(self):
        """
        Test that created_at is a datetime object.
        """
        self.assertIsInstance(self.place.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """
        Test that updated_at is a datetime object.
        """
        self.assertIsInstance(self.place.updated_at, datetime)

    def test_str_method(self):
        """
        Test the __str__ method.
        """
        string_rep = f"[Place] ({self.place.id}) {self.place.__dict__}"
        self.assertEqual(str(self.place), string_rep)

    def test_save_method(self):
        """
        Test the save method.
        """
        old_updated_at = self.place.updated_at
        self.place.save()
        self.assertNotEqual(self.place.updated_at, old_updated_at)

    def test_to_dict_method(self):
        """
        Test the to_dict method.
        """
        place_dict = self.place.to_dict()
        self.assertEqual(place_dict["__class__"], "Place")
        self.assertEqual(place_dict["id"], self.place.id)
        self.assertEqual(place_dict["created_at"],
                         self.place.created_at.isoformat())
        self.assertEqual(place_dict["updated_at"],
                         self.place.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
