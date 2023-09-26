#!/usr/bin/python3
"""This does serialization and deserialiazation"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """File storage class for storing instances of a dictionary through json"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """all method to return dictionary of the class attribute"""

        if cls is not None:
            given_obj_dict = {}
            for a, b in self.__objects.items():
                if cls is type(b):
                    given_obj_dict[a] = b
            return given_obj_dict
        elif cls is None:
            return self.__objects

    def new(self, obj):
        """this method sets in the private object obj as the
        object and the key"""

        if obj is not None:
            stringg = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[stringg] = obj

    def save(self):
        """serializes the object which is a dictionary"""

        dict_jfile = {}
        for k, v in self.__objects.items():
            dct = v.to_dict()
            dict_jfile[k] = dct

        with open(FileStorage.__file_path, "w", encoding="utf-8") as file1:
            jstr = json.dumps(dict_jfile)
            file1.write(jstr)

    def reload(self):
        """reload method to ressurate the object intstance dictionary"""

        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as file1:
                txt = file1.read()
                json_conv = json.loads(txt)
                for key, value in json_conv.items():
                    class_name, obj_id = key.split('.')
                    cls = eval(class_name)
                    ins = cls(**value)
                    self.__objects[key] = ins

    def delete(self, obj=None):
        """to delete obj from __objects if its inside"""

        if obj is not None:
            found = False
            for a, b in self.__objects.items():
                if b is obj:
                    to_del = a
                    found = True
            if found is True:
                del self.__objects[to_del]
                del obj
