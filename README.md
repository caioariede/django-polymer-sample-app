djogging
========

A sample app written in [Django](http://djangoproject.com) and [Polymer](https://www.polymer-project.org/1.0/).

**What does it do?**

- User signin/signup/logout
- Time tracking (insert date, time and distance)
- Reports (distance & avg. speed per week)


Installation
------------

    pip install -r requirements.txt
    python manage.py migrate


Admin
-----

You must create a superuser:

    python manage.py createsuperuser

Then access:

    http://localhost:port/admin/


REST API
--------

It's available in: http://localhost:port/rest-track/

