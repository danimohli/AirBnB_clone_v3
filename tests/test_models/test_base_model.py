import unittest
from datetime import datetime
from models.base_model import BaseModel
import uuid
import time


class TestBaseModel(unittest.TestCase):
    """
    Test cases for the BaseModel class.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        self.model = BaseModel()

    def test_instance_creation(self):
        """
        Test that a new instance is correctly created.
        """
        self.assertIsInstance(self.model, BaseModel)
        self.assertIsInstance(self.model.id, str)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_unique_id(self):
        """
        Test that each instance has a unique id.
        """
        another_model = BaseModel()
        self.assertNotEqual(self.model.id, another_model.id)

    def test_str_method(self):
        """
        Test the __str__ method.
        """
        expected_str = f"[BaseModel] ({self.model.id}) {self.model.__dict__}"
        self.assertEqual(str(self.model), expected_str)

    def test_to_dict(self):
        """
        Test the to_dict method.
        """
        model_dict = self.model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertEqual(model_dict['id'], self.model.id)
        self.assertEqual(model_dict['created_at'],
                         self.model.created_at.isoformat())
        self.assertEqual(model_dict['updated_at'],
                         self.model.updated_at.isoformat())

    def test_save_method(self):
        """
        Test the save method.
        """
        old_updated_at = self.model.updated_at
        time.sleep(0.1)  # Sleep to ensure updated_at is changed
        self.model.save()
        new_updated_at = self.model.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertGreater(new_updated_at, old_updated_at)

    def test_kwargs_creation(self):
        """
        Test creating an instance with kwargs.
        """
        model_dict = self.model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertEqual(new_model.id, self.model.id)
        self.assertEqual(new_model.created_at, self.model.created_at)
        self.assertEqual(new_model.updated_at, self.model.updated_at)
        self.assertEqual(new_model.__str__(), self.model.__str__())

    def test_kwargs_creation_exclude_class(self):
        """
        Test creating an instance with kwargs and ensure
        __class__ is excluded.
        """
        model_dict = self.model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertNotIn('__class__', new_model.__dict__)

    def test_datetime_conversion(self):
        """
        Test that created_at and updated_at are converted
        back to datetime objects.
        """
        model_dict = self.model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertIsInstance(new_model.created_at, datetime)
        self.assertIsInstance(new_model.updated_at, datetime)

    def test_id_is_string(self):
        """
        Test that id is a string.
        """
        self.assertIsInstance(self.model.id, str)

    def test_created_at_is_datetime(self):
        """
        Test that created_at is a datetime object.
        """
        self.assertIsInstance(self.model.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """
        Test that updated_at is a datetime object.
        """
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_created_at_equals_updated_at_on_creation(self):
        """
        Test that created_at and updated_at are
        equal upon instance creation.
        """
        self.assertEqual(self.model.created_at, self.model.updated_at)

    def test_kwargs_creation_with_extra_attributes(self):
        """
        Test creating an instance with kwargs and additional attributes.
        """
        model_dict = self.model.to_dict()
        model_dict['new_attr'] = 'new_value'
        new_model = BaseModel(**model_dict)
        self.assertEqual(new_model.new_attr, 'new_value')


if __name__ == '__main__':
    unittest.main()
