Mnemosyne: a micro service to save bookmarks as PyBossa tasks
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


Configuring the micro-service
=============================

The software comes with a settings.py.tmpl file, in the **links** folder, with a 
mininum configuration. Please, copy it and rename the copy to **settings.py**.
Then modify it according to your needs.

When you have the file configures, you are ready to start the service:

 python links/web.py

And a server in http://localhost:5000 will be available and ready for you.


Deploying the service with Apache2
==================================

You need to install Apache2 and mod-wsgi to deploy the service (or use other
servers like Nginx, gunicorn, etc.). In this case, we show how you can deploy
it using the well known Apache2 server.

This section explains how you can install the service in an Ubuntu machine.

Install the following packages:

 $ sudo apt-get install apache2 libapache2-mod-wsgi

After installing the softwre, you have to enable the mod-wsgi library and
restart the web server:

 $ sudo a2enmod wsgi
 $ sudo service apache2 restart

Now you have to create a virtual host for hosting the micro-service. In the
**contrib/apache2** folder you can find a template that you can re-use:

 <VirtualHost *:80>
    ServerName example.com

    DocumentRoot /home/user/Mnemosyne
    WSGIDaemonProcess Mnemosyne user=user1 group=group1 threads=5
    WSGIScriptAlias / /home/user/Mnemosyne/contrib/Mnemosyne.wsgi

    <Directory /home/user/Mnemosyne>
        WSGIProcessGroup Mnemosyne
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
 </VirtualHost>

You can specify a user and group from your machine with lower privileges in order to 
improve the security of the site. You can also use the www-data user and group name.

Once you have adapted the PATH in that file, copy it into the folder:

 /etc/apache2/sites-available

Enable the site:

 $ sudo a2ensite Mnemosyne

And restart the server:

 $ sudo service apache2 restart
 
Now the server is configured and app. Enjoy!

Deploying the service witn Nginx and uwsgi
==========================================

You can also deploy the web service using Nginx and uwsgi. The contib folder
has two templates that you can easily adapt to deploy it.

Copy the **contrib/uwsgi/mnemosyne.ini.tmpl** template, and rename it to
**mnemosyne.ini**. Then modify the values to match your paths, name, etc.

You can then run the service with the following command (without even
activating the virutal environment):

```bash
   $ cd yourapplicationpath
   $ env/bin/uwsgi contrib/uwsgi/mnemosyne.ini
```

If the command runs successfully, you should be able to see that two sockets
are created:

* **/tmp/mnemosyne.sock**
* **/tmp/mnemosyne-stats.sock**

The first one is the web service, the second one is the uwsgi stats socket for
analyzing the performance of your config file. Once you are happy with it, use
[Supervisord](http://supervisord.org/) for running the service automatically,
or if you prefer, create an init.d script.

Then, copy the **contrib/nginx/mnemosyne.conf.tmpl** to **mnemosyne.conf**
file, adapt it, and place it in the nginx site folder (*note*: this varies
between distributions, in Ubuntu or Debian based ones, the folder is
*/etc/nginx/sites-available* and then a symlink into */etc/nginx/sites-enabled*
in order to enable it). Restart nginx and the service should be available.
