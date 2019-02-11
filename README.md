# simpleNDB

[![Travis CI](https://travis-ci.org/runette/simpleNDB.svg?branch=master&style=flat)](https://travis-ci.org/runette/simpleNDB)
[![Python versions](https://img.shields.io/pypi/pyversions/simpleNDB.svg)](https://pypi.python.org/pypi/simpleNDB)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/runette/simpleNDB/blob/master/LICENSE)
[![Known Vulnerabilities](https://snyk.io/test/github/runette/simpleNDB/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/runette/simpleNDB?targetFile=requirements.txt)

## Purpose
Provides a set of wrappers for the Google Cloud Python clients to be used on Python 3 App Engine Standard Edition instances to provide some of the abilities previously provided by the appengine api and ext libraries.

## Installation

```shell
$ pip install simpleNDB
```

The full package can be imported as follows:

```python
from simplendb import ndb, images, users
```

To use the individual components, see :

- [NDB](docs/NDB.md)
- [Users](docs/USERS.md)
- [Images](docs/IMAGES.md)

## Background and Concepts

I needed to migrate some simple applications running on the  Google Appengine Standard Edition Python 2 version to the Python 3 version.

This is a major change to the runtime environment - involving a complete change to the webserver and python run time environments. It also sunsets a number of very usefull APIs that made it very quick and easy to run up a simple web app or web site for groups, for demonstrations and for prototypes : **including** :

- **NDB** - A simple NoSQL Network Database built on Cloud Datastore. Quick and easy to set up a schema.
- **Users** - A simple, no setup way to authenticate users against their Google id and get the details. Allows you to create authenticated apps without effort.
- **Blobstore** - a handy and simple way of storeing blobs and images.
- **Images** - an inbuilt image handler optimised for the environment. Included the native __get_serving_url function that it loosk like will not be resurected :angry:

There are, of course, ways to do the same thinsg in the new environment, since all that has gone away is effectively middle ware. Google recommend the following:

- The [**Google Cloud Python Clients**](https://pypi.org/project/google-cloud-datastore/) to access the datastore database
- The [**Firebase Auth API**](https://firebase.google.com/products/auth/)
- Using [Pillow](https://python-pillow.org/) for images

This is all actually very good, but as one commentor said :

> this requires the developer to create a lot of boilerplate that the appengine API used to do for us

This library is an attempt to do the boilerplate and make these libraries more of a drop-in replacement for the old libraries. I am not attempting to do a **full** drop-in replacement - there are attempts to do this for NDB for instance [see](https://github.com/googleapis/google-cloud-python/tree/master/ndb) but that looks like it will take 10 months and I needed somthing in 2 days. That *something* is this library. Quick and not very clean but good for the sort of simple apps that AppEngine SE should be good for. 

It basically allows developers to migrate basic current apps to use the Google Cloud Clients without completely restructuring the app. There will be some format and type changes and if you want advanced capabilities (like transactions and async operations) you should probable wait for the library linked above or do a proper migration of your app.
