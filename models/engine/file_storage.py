#!/usr/bin/python3
"""
Serializes and deserializes instances to and from JSON file
"""
import json
import models
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.state import State

classes = {"BaseModel": BaseModel, "User": User, "Place": Place,
           "City": City, "Amenity": Amenity, "Review": Review, "State": State}


class FileStorage:
    """Serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary __objects"""
        if cls:
            (return {k: v for k, v in self.__objects.items()
             if isinstance(v, cls)})
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        with open(self.__file_path, 'w') as f:
            temp = {k: v.to_dict(include_password=True)
                    for k, v in self.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                for key, value in temp.items():
                    self.__objects[key] = classes[value["__class__"]](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it's inside"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
