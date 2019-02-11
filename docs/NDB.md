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

- Description
- Exclusions
- Authentication
- Reference
- Migration from AppEngine
- Other Run Time environments
- Dev Environment

## Description

The [NDB library](https://cloud.google.com/appengine/docs/standard/python/ndb/) (written by Guido) was a NoSQL database library running on top of [Google Cloud Datastore](https://cloud.google.com/datastore/docs/concepts/overview) was provided out-of-the-box in the Python 2.7 AppEngine runtime - making it a simple way of providing object persistence to web apps and cloud functions without a lot of boilerplate work.

This library has been sunsetted in the Python 3.7 version of AppEngine Standard Edition. The Google Cloud Datastore Client do a good job of providing the basic functionality of Datastore and thus compatibility with entities created in NDB. It provides some basic functions we need:

- **Works with NDB created entities** There are some exceptions - The Google Datastore client only works with *datetime* and not either *date* or *time* for instance ([see](https://googleapis.github.io/google-cloud-python/latest/datastore/entities.html))
- **Provides the basic functions** /- i.e. `get()`, `put()`, `delete()` and `query()`
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

which is a sub-class of the Google Cloud Client [`Entity`]() class. 

## Migration from AppEngine

There are a number of key differences :

1 The Class definition is different.

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

as described in the reference. This is actually quite a simple mechanical edi from the NDB equivalent which would have been :

```python
gunid = ndb.IntegerProperty()
```

- Queries, filters and order. SimpleNBD follows the Datastore [formats](https://googleapis.github.io/google-cloud-python/latest/datastore/queries.html) filters are 3-tuples :`('<property>', '<operator>', <value>)`; and the order attribute is on the Query constructor and not a seperate method.

So an NDB Query command :

```python
Gun.query(Gun.type==Gun.Types.BRONZE).order(Gun.gunid).fetch()
```

becomes

```python
Gun.query(filters=[("type", "==",Gun.Types.BRONZE)], order=[gunid]).fetch()
```

- Transactions. This model does not touch the Google Cloud Client approach to transactions. I have not tried any migrations to know what that involves.

## Other Run Time Environments

This library and it's dependencies do **NOT** have anydependency on the Google Cloud Platform (i.e. AppEngine and ComputeEngine) to run. Therefore, this migration would also work for migration to other platforms.

Obviously, you still need a GCP project to provide the Google Cloud Datastore instance and credentials. You also need to make sure that those cedentials are registered to the Client in the same way as for the Dev environment below.

## Dev Environment

As part of the change to Python 3 and idiomatic use of Python - you also do not have dev_appserver anymore. This means more work setting up the dev environment.

The Google Cloud SDK does provide a datastore local emulator for this purpose - available [here](https://cloud.google.com/datastore/docs/tools/datastore-emulator). This works well - although I found that it is best to launch it directly rather than through the SDK since it needs to know how to auto-create ids. Without this - `puts()` will fail without a user generated key. You need to set the --auto_id_policy=SEQUENTIAL switch.

For authentication - you need to create and download a JSON token for the service account for your GCP project from the console.

You need to set the follwoing environments variables to tell it how to authenticate and to use the emulator rather than the remote service :

'''shell
GOOGLE_CLOUD_PROJECT = {{YOUR_GCP_PROJECT_ID}}
GOOGLE_APPLICATION_CREDENTIALS = {{PATH_TO_AND_NAME_OF_THE_JSON_TOKEN}}
DATASTORE_DATASET=ultima-ratio-221014
DATASTORE_EMULATOR_HOST=localhost:{{PORT_NUMBER_PROVIDED_BY_THE_EMULATIR}} 
DATASTORE_EMULATOR_HOST_PATH={{PATH_PROVIDED_BY_THE_EMULATOR}}
DATASTORE_HOST=http://localhost:{PORT_NUMBER_PROVIDED_BY_THE_EMULATOR}}
DATASTORE_PROJECT_ID={{YOUR_GCP_PROJECT_ID}}
