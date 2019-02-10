# simpleNDB

## Purpose
Provides a set of wrappers for the Google Cloud Python clients to be used on Python 3 App Engine Standard Edition instances to provide some of the abilities previously provided by the appengine api and ext libraries.

## Installation

```shell
$ pip install simplendb
```

The full package can be imported as follows:

```python
from simplendb import ndb, images, users
```

To use the individual components, see :

- [NDB](docs/NDB.md)
- [Users](docs/Users.md)
- [Images](docs/Images.md)

## Background and Concepts

I needed to migrate some simple applications running on the  Google Appengine Standard Edition Python 2 version to the Python 3 version.

This is a major change to the runtime environment - involving a complete change to the webserver and python run time environments. It also sunsets a number of very usefull APIs that made it very quick and easy to run up a simple web app or web site for groups, for demonstrations and for prototypes : **including** :

- **NDB** - A simple NoSQL Network Database built on Cloud Datastore. Quick and easy to set up a schema.
- **Users** - A simple, no setup way to authenticate users against their Google id and get the details. Allows you to create authenticated apps without effort.
- **Blobstore** - a handy and simple way of storeing blobs and images.
- **Images** - an inbuilt image handler optimised for the environment. Included the native __get_serving_url function that it loosk like will not be resurected :frowning
