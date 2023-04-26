#!/usr/bin/python3
"""
Database storage class
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ database model """
    __engine = None
    __session = None

    def __init__(self):
        """ connect to db """
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, passwd, host, db),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ list all entries """
        obj_dict = {}
        if cls:
            all_objects = self.__session.query(cls).all()
            for obj in all_objects:
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                obj_dict[key] = obj
        else:
            obj_list = [User, State, City, Amenity, Place, Review]
            for obj in obj_list:
                all_objects = self.__session.query(obj).all()
                for obj in all_objects:
                    key = '{}.{}'.format(obj.__class__.__name__,
                                         obj.id)
                    obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """ add new item """
        self.__session.add(obj)

    def save(self):
        """ save changes """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ reload """
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """ Remove private session attribute """
        self.__session.close()
