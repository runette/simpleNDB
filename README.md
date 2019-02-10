# simpleNDB

## Purpose
Provides a set of wrappers for the Google Cloud Python clients to be used on Python 3 App Engine Standard Edition instances to provide some of the abilities previously provided by the appengine api and ext libraries.

## Installation

```
$ pip install simplendb
```

The full package can be imported as follows:

```
**from** simplendb **import** ndb, images, users
```


## Background and Concepts

I needed to migrate some simple applications running on the  Google Appengine Standard Edition Python 2 version to the Python 3 version.

This is a major change to the runtime environment - involving a complete change to the webserver and python run time environments. It also sunsets a number of very usefull APIs that were 
