# NDB Module

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


gun = Gun()
gun.gunid = 12
gun.name = "This is a name"
gun.type = Gun.Type.WROUGHT
gun.put()
```

# Table of Contents

- [Description](https://github.com/runette/simpleNDB/blob/master/docs/NDB.md#description)
- [Exclusions](https://github.com/runette/simpleNDB/blob/master/docs/NDB.md#exclusions)
- [Authentication](https://github.com/runette/simpleNDB/blob/master/docs/NDB.md#authentication)
- [Reference](https://github.com/runette/simpleNDB/blob/master/docs/NDB.md#reference)
- [Migration from AppEngine](https://github.com/runette/simpleNDB/blob/master/docs/NDB.md#other-run-time-environments)
- [Other Run Time environments](https://github.com/runette/simpleNDB/blob/master/docs/NDB.md#other-run-time-environments)
- [Dev Environment](https://github.com/runette/simpleNDB/blob/master/docs/NDB.md#dev-environment)

## Description

The [NDB library](https://cloud.google.com/appengine/docs/standard/python/ndb/) (written by Guido) is a NoSQL database library running on top of [Google Cloud Datastore](https://cloud.google.com/datastore/docs/concepts/overview) is was provided out-of-the-box in the Python 2.7 AppEngine runtime - making it a simple way of providing object persistence to web apps and cloud functions without a lot of boilerplate work.

This library has been sunsetted in the Python 3.7 version of AppEngine Standard Edition. The Google Cloud Datastore Client do a good job of providing the basic functionality of Datastore and thus compatibility with entities created in NDB. It provides some basic functions we need:

- **Works with NDB created entities** There are some exceptions - The Google Datastore client only works with *datetime* and not either *date* or *time* for instance ([see](https://googleapis.github.io/google-cloud-python/latest/datastore/entities.html))
- **Provides the basic functions** - i.e. `get()`, `put()`, `delete()` and `query()`
- **provides ACID transactions**

However, the resulting code does not match the way that NDB worked and is quite a task to migrate. The Entities are subclassed Dicts and only take the ['name'] notation and do not have a schema. We need :

- The ability to created schema'ed entity classes
- the ability to use the .attribute notation
- some consistency about how to migrate from NDB

That is what this library provides.

## Exclusions

This library does **not** attempt to provide :

- Direct drop-in code compatibility.
- Expanso types of schema - just use the native Google Datastore Client
- Async get() or put() or any in-memory cacheing or optimization. This is not intended for high-performance installations.
- support for any version of Python before 3.4 - since that is the whole point!

Currently - it does not provide the following types of properties. This may be changed in the future:

- DateProperty and TimeProperty
- BlobProperty
- StructuredProperty
- PickleProperty


## Authentication

Using the datastore requires the app to be authenticated to the datastore server. This is all done by the Google Cloud Client and is [explained in that documentation](https://googleapis.github.io/google-cloud-python/latest/core/auth.html).

The key phrase is :

> If you’re running in Compute Engine or App Engine, authentication should “just work”.

In other environments you have to tell it where to find the credentials. This may include the debug and test environments.

## Reference

### Model class
#### Definition

This class is used as the parent for all simpleNDB Entity classes and is a sub-class of the Google Cloud Client [`Entity`](https://googleapis.github.io/google-cloud-python/latest/datastore/entities.html) class.

The Model class requires that you set up a schema in the Entity class definition as follows 

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

The schema is defined in the in the `schema()` method. There should be one line per property of the format :

```python
self.Property("NAME_OF_PROPERTY", "PROPERTY_TYPE", **kwargs)
```
where PROPERTY_TYPE is defined by:

```python
class ndb(Enum):
    IntegerProperty = (0, True, int)
    FloatProperty = (1, False, float)
    StringProperty = (2, True, str)
    TextProperty = (3, False, str)
    BooleanProperty = (4, True, bool)
    DateTimeProperty = (5, True, datetime)
    GeoPtProperty = (6, True, GeoPt)
    KeyProperty = (7, True, Key)
    JsonProperty = (8, False, str)
    EnumProperty = (9, True, int)
```
and `**kwargs` are :

```python
repeated=True|False
indexed=True|False
default=
auto_now=True|False
```

as per [NDB](https://cloud.google.com/appengine/docs/standard/python/ndb/entity-property-reference).

The EnumProperty takes and addition key-word :

```python
enum=
```
giving the class for an enum which must be of type `enum` (and not `messages.ENUM`).

#### Usage

The Object entities are used in a similar way to the usage in NDB and keep all of the methods described in the Google Cloud Client `Entity` definition:

```Python
gun = Gun()
gun.gunid = 12
gun.name = "This is a name"
gun.type = Gun.Type.WROUGHT
name = gun.name
gun.put()
```

As with NDB - the enitity is not persisted until `put()` is called. All properties can be called using Object.attribute notation and that will keep the schema typing (i.e. enums are enums etc). The base object is a Dict so you can access the native Datastore values using the .['name'] notation.

The `items()` method has been intercepted and will only provide a Dict copy of the values of the schema properties (and no other properties or members). These are also the only values that will be persisted.

### Query Class
#### Definition 

The Query class is used to run queries and is as documented in the [Google Cloud Client documentation](https://googleapis.github.io/google-cloud-python/latest/datastore/queries.html).

#### Usage

Always create the query object using the `.query()` method on the Entity class - i.e. :

```python
Gun.query(filters=[("type", "==",Gun.Types.BRONZE)], order=[gunid]).fetch()
```
### Key Class
#### Definition 

The Key class is an immutable representation of a datastore Key. and is as documented in the [Google Cloud Client documentation](https://googleapis.github.io/google-cloud-python/latest/datastore/keys.html).

simpleNDB makes one addition the Key class - providing a `get()` method to allow the entity to be fetched from the datastore.

Note that - is you fetch keys from querries they may be of type `datastore.Key` and not `ndb.Key` and then they will not have the `get()` method. You will need to do the conversion.


## Migration from AppEngine NDB

There are a three areas that need to be changed, described below.

* The Class definition is different.

- The Object class must be a sub-class of ndb.Model 
- In SimpleNDB (for simplicity at my end) - the schema is defined in a method called `schema()`. This must be overloaded by the sub-clas and start :

```python
def schema(self):
        super().schema()
```

and then has a line for each member of the schema of the form :

```python
self.Property("gunid", ndb.IntegerProperty)
```

as described in the reference. This is actually quite a simple mechanical edit from the NDB equivalent which would have been :

```python
gunid = ndb.IntegerProperty()
```

* Queries, filters and order. SimpleNBD follows the Datastore [formats](https://googleapis.github.io/google-cloud-python/latest/datastore/queries.html) filters are 3-tuples :`('<property>', '<operator>', <value>)`; and the order attribute is on the Query constructor and not a seperate method.

So an NDB Query command :

```python
Gun.query(Gun.type==Gun.Types.BRONZE).order(Gun.gunid).fetch()
```

becomes

```python
Gun.query(filters=[("type", "==",Gun.Types.BRONZE)], order=[gunid]).fetch()
```

* Transactions. This model does not touch the Google Cloud Client approach to transactions. I have not tried any migrations to know what that involves.

## Other Run Time Environments

This library and it's dependencies do **NOT** have any dependency on the Google Cloud Platform (i.e. AppEngine and ComputeEngine) to run. Therefore, this approach would also work for migration to other platforms.

Obviously, you still need a GCP project to provide the Google Cloud Datastore instance and credentials. You also need to make sure that those credentials are registered to the Client in the same way as for the Dev environment below.

## Dev Environment

As part of the change to Python 3 and idiomatic use of Python - you also do not have dev_appserver anymore. This means more work setting up the dev environment.

The Google Cloud SDK does provide a datastore local emulator for this purpose - available [here](https://cloud.google.com/datastore/docs/tools/datastore-emulator). This works well - although I found that it is best to launch it directly rather than through the SDK since it needs to know how to auto-create ids. Without this - `puts()` will fail without a user generated key. You need to set the --auto_id_policy=SEQUENTIAL switch.

For authentication - you need to create and download a JSON token for the service account for your GCP project from the console.

You need to set the following environments variables to tell it how to authenticate and to use the emulator rather than the remote service :

```shell
GOOGLE_CLOUD_PROJECT = {{YOUR_GCP_PROJECT_ID}}
GOOGLE_APPLICATION_CREDENTIALS = {{PATH_TO_AND_NAME_OF_THE_JSON_TOKEN}}
DATASTORE_DATASET={{PROVIDED_BY_EMULATOR}}
DATASTORE_EMULATOR_HOST=localhost:{{PORT_NUMBER_PROVIDED_BY_THE_EMULATIR}} 
DATASTORE_EMULATOR_HOST_PATH={{PATH_PROVIDED_BY_THE_EMULATOR}}
DATASTORE_HOST=http://localhost:{PORT_NUMBER_PROVIDED_BY_THE_EMULATOR}}
DATASTORE_PROJECT_ID={{YOUR_GCP_PROJECT_ID}}
```
