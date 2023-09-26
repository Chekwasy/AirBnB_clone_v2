#!/usr/bin/python3
"""class city that inherit from basemodel for city name etc"""
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models import storage_t


class City(BaseModel, Base):
    """The class city begins"""

    if storage_t == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities")
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """Initialization for city"""

        super().__init__(*args, **kwargs)
