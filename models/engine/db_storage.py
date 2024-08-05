#!/usr/bin/python3
"""
Database storage engine
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.state import State
import os

classes = {"BaseModel": BaseModel, "User": User, "Place": Place,
           "City": City, "Amenity": Amenity, "Review": Review, "State": State}


class DBStorage:
    """Database storage engine for MySQL storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, passwd, host, db), pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session all objects
        depending on the class name"""
        new_dict = {}
        if cls:
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                new_dict[key] = obj
        else:
            for clss in classes.values():
                for obj in self.__session.query(clss).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
