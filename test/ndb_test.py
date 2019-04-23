import pytest
import json, types, sys
from enum import Enum
from datetime import datetime
import logging
from simplendb.ndb import Model, Query, Key, GeoPt, ndb
from simplendb.users import UserStatus
from simplendb.images import ndbImage
from simplendb.helpers import to_bool, to_int



class Gun(Model):
    class Types(Enum):
        CAST = 0
        WROUGHT = 1
        BRONZE = 2
        NOT_KNOWN = 3
    class Quality(Enum):
        GOLD = 2
        SILVER = 1
        BRONZE = 0

    def schema(self):
        super().schema()
        self.Property("gunid", ndb.IntegerProperty)
        self.Property("location", ndb.GeoPtProperty)
        self.Property("type", ndb.EnumProperty, enum=Gun.Types)
        self.Property("quality", ndb.EnumProperty, enum=Gun.Quality,  default=Gun.Quality.BRONZE)
        self.Property("description", ndb.StringProperty)
        self.Property("name", ndb.StringProperty)
        self.Property("date", ndb.DateTimeProperty, auto_now=True)
        self.Property("site", ndb.StringProperty)
        self.Property("context", ndb.StringProperty)
        self.Property("collection", ndb.BooleanProperty)
        self.Property("coll_name", ndb.StringProperty)
        self.Property("coll_ref", ndb.StringProperty)
        self.Property("images", ndb.TextProperty, repeated=True)
        self.Property("markings", ndb.BooleanProperty)
        self.Property("mark_details", ndb.StringProperty)
        self.Property("interpretation", ndb.BooleanProperty)
        self.Property("inter_details", ndb.StringProperty)
        self.Property("country", ndb.StringProperty, default="none")
        self.Property("geocode", ndb.JsonProperty)
        self.Property("neighbour", ndb.KeyProperty, repeated=True)

def test_1():
    gun = Gun()
    assert gun.quality == Gun.Quality.BRONZE
    assert gun.images == []
    assert gun.key.kind == 'Gun'
    assert type(gun) == gun
    assert type(gun.get_key()) == Key
    assert gun.date.year == datetime.now().year
    gun.location = GeoPt(52, 1)
    gun.geocode =  {'test': 'name','test2': 'name2' }
    gun.put()
    Gun.get_by_id(gun.key.id)
    assert gun.quality == Gun.Quality.BRONZE
    assert gun.images == []
    assert gun.key.kind == 'Gun'
    assert type(gun) == gun
    assert type(gun.get_key()) == Key
    assert gun.date.year == datetime.now().year
    assert gun.location == GeoPt(52,1)
    assert gun.geocode == {'test': 'name','test2': 'name2' }
    gun.delete()
