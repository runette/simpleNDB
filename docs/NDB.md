# simpleNDB.NDB Module

## Purpose

This module provides wrappers to the [Google Cloud Datastore Client](https://googleapis.github.io/google-cloud-python/latest/datastore/index.html) library to make it work more like the appengine NDB library.

## Installation

```python
from simplendb.ndb import Model, Query, Key, GeoPt, ndb
```

### Typical Usage

```python
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
        self.Property("images", ndb.TextProperty, repeated=True)
        self.Property("markings", ndb.BooleanProperty)
        self.Property("interpretation", ndb.BooleanProperty)
        self.Property("country", ndb.StringProperty, default="none")
        self.Property("geocode", ndb.JsonProperty)
        
```
