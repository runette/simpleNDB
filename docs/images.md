# images Module
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

The Python 2.7 edition of Google AppEngine Standard Edition included an out of the box [Image](https://cloud.google.com/appengine/docs/standard/python/refdocs/google.appengine.api.images#google.appengine.api.images.Image) class that made it esy to do simple actions on Images.

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

The Blob class is used as a container for the objects stored on[Google Cloud Storage](https://cloud.google.com/storage/). The Blob class contains an instance of a [Google Cloud Storage Client](https://googleapis.github.io/google-cloud-python/latest/storage/index.html) [Blob](https://googleapis.github.io/google-cloud-python/latest/storage/blobs.html) class.

The only methods on this class are:

- The constructor requires `Blob(name, bucket)` - where the name is the name of the object which can be "dev/1/filename.jpg" as per the Cloud Storage docs) and the bucket is the name of the bucket. To create a new object - just use a new name and it will be created.
- The class has `get()` and `put.()` methods to get from and put to Cloud Storage.

`get()` returns an io.ByteIO object. 
`put()` requires an io.ByteIO object.

#### Usage

```python
 blob = Blob(full_path, bucket_name)
      stream =  blob.get()
      blob.put(stream)
```

### ndbImage Class
#### Definition

The ndbImage Class is an Object that holds both a blob and a Pillow Image class.

When the object is created - it creates a Blob class as a `.blob` property.

As a aresult of a `.get()` call, the Storage object is downloaded and made into a Pillow Image class object and stored as the `.image` property.

A `put()` call on the ndbImage will result in the `.image` property being uploaded to the Storage object.

All Pillow functions can be done on the `.image` property as normal - e.g:

```python
original.image.thumbnail(size)
```

ndbImage also provides the following methods:

- `resize(size, target_object_name)` - runs a Pillow resize on the image and returns a new ndbImage object with the resized image in the same bucket but using the name given as `target_object_name`. Remember to use `put()` to save this object.

- `get_media_link()` - gets the Cloud Storage public media access URL for this object.

#### Formats

Image formats and types get a bit complicated.

All Cloud Storage items need a 

are as per the [Pillow docs](https://pillow.readthedocs.io/en/3.1.x/reference/Image.html). The 

#### Usage

```python
image = ndbImage("dev/1/image.jpeg",my_bucket_name)
image.get()
image_32 = image.resize((32,32), "dev/1/image_32.jpeg")
image_32.put()
```


