#!/usr/bin/python3
"""
Python class called base_model that has the methods attribute
and instances which other class will inherit from
"""
import uuid
from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


time = "%Y-%m-%dT%H:%M:%S.%f"
if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """
    The class BaseModel that defines all common attributes and
    methods for other classes
    """

    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization method for instance attributes"""

        kwargs_len = len(kwargs)
        if kwargs_len > 0 and kwargs is not None:
            for k, v in kwargs.items():
                if k != "__class__":
                    if k == "updated_at" or k == "created_at":
                        v = datetime.fromisoformat(v)
                    setattr(self, k, v)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """string representation of the instance"""

        st = "[" + str(self.__class__.__name__) + "]" + \
            " (" + self.id + ") " + str(self.__dict__)
        return st

    def to_dict(self):
        """ to dict"""

        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def save(self):
        """saving method to change the updated time"""

        if (self.updated_at):
            self.updated_at = datetime.now()
            models.storage.new(self)
            models.storage.save()

    def delete(self):
        """delete the current instance from the storage"""

        models.storage.delete(self)
