import unittest
from models.state import State
from datetime import datetime
import uuid


class TestState(unittest.TestCase):
    """
    Test cases for the State class.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        self.state = State()

    def test_instance_creation(self):
        """
        Test that an instance of State is created.
        """
        self.assertIsInstance(self.state, State)

    def test_attributes(self):
        """
        Test the attributes of the State class.
        """
        self.assertTrue(hasattr(self.state, "id"))
        self.assertTrue(hasattr(self.state, "created_at"))
        self.assertTrue(hasattr(self.state, "updated_at"))
        self.assertTrue(hasattr(self.state, "name"))
        self.assertEqual(self.state.name, "")

    def test_id_is_uuid(self):
        """
        Test that id is a valid UUID.
        """
        self.assertIsInstance(uuid.UUID(self.state.id), uuid.UUID)

    def test_created_at_is_datetime(self):
        """
        Test that created_at is a datetime object.
        """
        self.assertIsInstance(self.state.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """
        Test that updated_at is a datetime object.
        """
        self.assertIsInstance(self.state.updated_at, datetime)

    def test_str_method(self):
        '''
        Test the __str__ method.
        '''
        string_rep = f"[State] ({self.state.id}) {self.state.__dict__}"
        self.assertEqual(str(self.state), string_rep)

    def test_save_method(self):
        """
        Test the save method.
        """
        old_updated_at = self.state.updated_at
        self.state.save()
        self.assertNotEqual(self.state.updated_at, old_updated_at)

    def test_to_dict_method(self):
        '''
        Test the to_dict method.
        '''
        state_dict = self.state.to_dict()
        self.assertEqual(state_dict["__class__"], "State")
        self.assertEqual(state_dict["id"], self.state.id)
        self.assertEqual(state_dict["created_at"],
                         self.state.created_at.isoformat())
        self.assertEqual(state_dict["updated_at"],
                         self.state.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
