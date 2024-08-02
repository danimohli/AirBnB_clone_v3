#!/usr/bin/python3
import unittest
import os
import json
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestFileStorage(unittest.TestCase):
    """
    Test cases for the FileStorage class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up once for all tests.
        """
        cls.storage = FileStorage()
        cls.file_path = "file.json"

    def setUp(self):
        """
        Set up test environment.
        """
        self.storage._FileStorage__objects = {}

    def tearDown(self):
        """Tear down test environment."""
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass

    def test_all_returns_dict(self):
        """
        Test that all returns the __objects dictionary.
        """
        self.assertEqual(self.storage.all(),
                         self.storage._FileStorage__objects)

    def test_new(self):
        """
        Test that new adds an object to __objects.
        """
        base_model = BaseModel()
        self.storage.new(base_model)
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], base_model)

    def test_save(self):
        """
        Test that save properly saves objects to file.json.
        """
        base_model = BaseModel()
        self.storage.new(base_model)
        self.storage.save()
        with open(self.file_path, "r") as f:
            data = json.load(f)
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]["id"], base_model.id)

    def test_reload_no_file(self):
        """
        Test that reload doesn't raise an error if file doesn't exist.
        """
        try:
            self.storage.reload()
        except Exception as e:
            self.fail(f"reload raised {e} unexpectedly!")

    def test_reload(self):
        """
        Test that reload correctly deserializes JSON file to __objects.
        """
        base_model = BaseModel()
        self.storage.new(base_model)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, self.storage.all())
        self.assertIsInstance(self.storage.all()[key], BaseModel)

    def test_save_and_reload_multiple_classes(self):
        """
        Test save and reload with multiple different classes.
        """
        base_model = BaseModel()
        user = User()
        state = State()
        city = City()
        amenity = Amenity()
        place = Place()
        review = Review()

        objects = [base_model, user, state, city, amenity, place, review]

        for obj in objects:
            self.storage.new(obj)

        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()

        for obj in objects:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.assertIn(key, self.storage.all())
            self.assertIsInstance(self.storage.all()[key], obj.__class__)

    def test_file_path_is_private(self):
        """
        Test that __file_path is a private class attribute.
        """
        self.assertTrue(hasattr(FileStorage, '_FileStorage__file_path'))
        self.assertFalse(hasattr(FileStorage, 'file_path'))

    def test_objects_is_private(self):
        """
        Test that __objects is a private class attribute.
        """
        self.assertTrue(hasattr(FileStorage, '_FileStorage__objects'))
        self.assertFalse(hasattr(FileStorage, 'objects'))

    def test_serialization_format(self):
        """
        Test the format of the serialized JSON.
        """
        base_model = BaseModel()
        self.storage.new(base_model)
        self.storage.save()
        with open(self.file_path, "r") as f:
            data = json.load(f)
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]["__class__"], "BaseModel")
        self.assertEqual(data[key]["id"], base_model.id)
        self.assertEqual(data[key]["created_at"],
                         base_model.created_at.isoformat())
        self.assertEqual(data[key]["updated_at"],
                         base_model.updated_at.isoformat())

    def test_save_with_no_objects(self):
        """
        Test saving when there are no objects.
        """
        self.storage.save()
        with open(self.file_path, "r") as f:
            data = json.load(f)
        self.assertEqual(data, {})

    def test_reload_with_no_objects(self):
        """
        Test reloading when there are no objects in the file.
        """
        with open(self.file_path, "w") as f:
            json.dump({}, f)
        self.storage.reload()
        self.assertEqual(self.storage.all(), {})


if __name__ == '__main__':
    unittest.main()
