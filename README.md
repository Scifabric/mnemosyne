PyBossa-links: a micro service to save bookmarks as PyBossa tasks
=================================================================

This micro-service is a very simple Flask application that allows you to save
a URL as popular services like bit.ly or delicious.com.

The difference is that basically there is no authentication to save URLs, as
the goal of the application is to interact with a web browser extension that
will send the URL to analyze it in a later stage at a PyBossa server
application.

The service saves the URL, and in case the URL is already in the system, it
returns the same object but with the field **new** equal to False.

There is a minimum validation: no empty URLs, and a throttling interface to
avoid flooding of the service (check the settings file).

Installing the application
==========================

It is very simple, create a virtualenv and then, install the requirements:

 $ pip install -r requirements.txt


To start the service you can test it like this:

 python links/web.py

And a server in http://localhost:5000 will be available and ready for you.

Deploying the service with Apache2
==================================

This will be fullfilled soon.
