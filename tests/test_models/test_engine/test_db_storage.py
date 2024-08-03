#!/usr/bin/python3
"""
Test for db_storage
"""

import unittest
from models.engine.db_storage import DBStorage
from models.user import User
"""
Import other necessary models
"""


class TestDBStorage(unittest.TestCase):
    def setUp(self):
        """Set up for tests."""
        self.storage = DBStorage()
        self.storage.reload()

    def test_get(self):
        """Test the get method."""
        user = User(name="John Doe", email="john@example.com")
        self.storage.new(user)
        self.storage.save()
        retrieved_user = self.storage.get(User, user.id)
        self.assertEqual(user, retrieved_user)
        self.assertIsNone(self.storage.get(User, "nonexistent_id"))

    def test_count(self):
        """Test the count method."""
        initial_count = self.storage.count()
        user = User(name="John Doe", email="john@example.com")
        self.storage.new(user)
        self.storage.save()
        self.assertEqual(self.storage.count(), initial_count + 1)
        self.assertEqual(self.storage.count(User), 1)


if __name__ == "__main__":
    unittest.main()
