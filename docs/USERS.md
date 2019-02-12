# images Module
## Purpose

This module provides wrappers to the [Google Cloud Storage Client library](https://googleapis.github.io/google-cloud-python/latest/index.html)  and [Firebase Authenticaton](https://firebase.google.com/docs/) to give them some of the functionality of te appenegine users api and to work nicely together.

This library can work in any run time environment - not just GAE.

## Installation

```python
from simplendb.users import UserStatus
```

## Typical Usage

```python
  @app.route('/')
  def main_handler():
    user_data = UserStatus(request.cookies.get("token"))
    return render_template("index.html", 
                user_data= user_data,
                index= 1)
```
### Table of Contents

- [Description]()
- [Exclusions]()
- [Authentication]()
- [Reference]()
- [Dev Environment]()

### Description

The AppEngine Python 2.7 Standard Edition had a very useful [`users`](https://cloud.google.com/appengine/docs/standard/python/users/) api. This has gone away with the idiomatic paradigm of the Python 3.7 incarnation.

The new suggested paradigm for user authentication 
