# Users Module
## Purpose

This module provides wrappers to the Google Cloud Storage Client library  and Pillow to give them some of the functionality of te appenegine Images library and to work nicely together.

This library can work in any run time environment - not just GAE - but it is dependent on Google Cloud Storage backend for storage.

## Installation

```python
from simplendn.images install ndbImages, ndbBlob
```

## Typical Usage

```python
def get_serving_url(upload_metadata):
    bucket_name = upload_metadata.get('bucket')
    full_path = upload_metadata.get('fullPath')
    folder = full_path.replace('/original', '')
    original = ndbImage(full_path, bucket_name)
    original.get()
    thumb_32 = original.resize((32,32), folder + "/32x32")
    thumb_32.put()
    thumb_200 = original.resize((200,200), folder + "/200x200")
    thumb_200.put()    
    mediaLink = {"original": original.get_media_link, "s32": thumb_32.get_media_link, "s200": thumb_200.get_media_link}
    return mediaLink
```
### Table of Contents

- Description
- Exclusions
- Authentication
- Reference
- Dev Environement

### Description

The Python 2.7 edition of Google AppEngine Standard Edition included an out of the box Image class that made it esy to do simple actions on Images.

The new, idiomatic Python 3.7 edition of GAE does not include any environment specific libraries and APIs - so no Image class. The suggestion is to use [Pillow](https://python-pillow.org/) - which is much better but is not out-of-the box integrated into Google Cloud Storage and there is a bit of trial-and-error and boilerplate to do that integration.

This library does that integration out of the box.

## Exclusions

The GAE Image class included the excellent "real-time resizable" `_get_serving_url()` links (if you do not know what that means - don't worry because they have gone away).

Unfortunately - they are no longer available (as far as I know). Because of this - I have avoided putting in a `_get_serving_url()` method as this would lead to confusion. You can get get the public link from `get_media_link`.

## Authentication

Using Cloud Storage requires the app to be authenticated to the storage server. This is all done by the Google Cloud Client and is [explained in that documentation](https://googleapis.github.io/google-cloud-python/latest/core/auth.html).

The key phrase is :

>If you’re running in Compute Engine or App Engine, authentication should “just work”.

In other environments you have to tell it where to find the credentials. This may include the debug and test environments.

## Reference
### Blob Class
#### Definition

The Blob class is used as a container for the objects stored on[Google Cloud Storage](https://cloud.google.com/storage/). The Blob class is a sub-class of the [Google Cloud Storage Client](https://googleapis.github.io/google-cloud-python/latest/storage/index.html) [Blob](https://googleapis.github.io/google-cloud-python/latest/storage/blobs.html) class.

The only additions to the default class are:

- The constructor requires `Blob(name, bucket)` - where the name is the name of the object which can be "dev/1/filename.jpg" as per the Cloud Storage docs) and the bucket is the name of the bucket. To create a new object - just use a new name and it will be created.
- The class has `get()` and `put.()` methods to get from and put to Cloud Storage.

#### Usage

```python
 blob = Blob(full_path, bucket_name)
    original.get()
    original.put()
```

### ndbImage Class
#### Definition

The ndbImage Class is an Object that holds both a blob and a Pillow Image class.

When 
