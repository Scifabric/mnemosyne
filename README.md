# Mnemosyne: a micro service to save links as PyBossa tasks

This micro-service is a very simple Flask application that allows you to save
an image URL as a PyBossa task. This micro-service is very similar to popular sites
like bit.ly or delicious.com.

The main difference is that there is **no authentication to save URLs**, as
the goal of the application is to interact with a web [browser
addon](https://github.com/PyBossa/mnemosyne-addon) that
will send the URL to analyze it in a later stage at a PyBossa server
application. In other words, the purpose of this web service is to allow
anonymous contributions to create PyBossa tasks using a Firefox extension.

Furthermore, Mnemosyne can be configured to host different projects and save
the URLs according to a project. Projects act like folders for saved links.

The service saves the URL, and in case the URL is already in the system, it
returns the same object but with the field **new** equal to False.

There is a minimum validation: no empty URLs, and a throttling interface to
avoid abusing the service (check the settings file).

# Requirements

 * Python >= 2.7
 * Redis >= 2.6

We recommend you to have the *build-essential* package for Debian/Ubuntu distributions
installed, as the next section will compile some software in order to work.

# Installing the application

It is very simple, create a virtualenv and then, install the requirements:

 $ cd pathapplication
 $ source env/bin/activate
 $ pip install -r requirements.txt

Now you have to init the DB:

```bash
    $ python create_db.py
```

That command should create a file named **links.db** in the mnemosyne folder.
Check it is there, before continuing. 

Finally, you have to add a project to Mnemosyne in order to allow users to
submit links for a given project using the [Firefox
addon](https://github.com/PyBossa/mnemosyne-addon):

```bash
    $ python project.py -n "Example project" -s "exampleproject" -k "keyword1,
    keyword2, keyword3, ..., keywordN" -p pybossa_app_short_name
```

The project will be created, and you will be able to see it with a Sqlite
browser or using the web service. We recommend to use [sqlitebrowser](http://sqlitebrowser.sourceforge.net/) 
as it is very simple and easy to use.

# Configuring the micro-service

The software comes with a settings.py.tmpl file, in the **links** folder, with a 
mininum configuration. Please, copy it and rename the copy to **settings.py**.
Then modify it to your needs.

When you have the file configured, you are ready to start the service in debug
mode:

 python links/web.py

The command will fire a web server at http://localhost:5000.

**NOTE**: We strongly recommend you to use a proper deployment solution like
Apache or Nginx if you plan to use it in a production service. Check the
following two sections. We recommend Nginx and uwsgi, at the bottom there is
also a solution for Apache.

# Deploying the service witn Nginx and uwsgi

You can deploy the web service using [Nginx](http://nginx.org/) and [uwsgi](http://uwsgi-docs.readthedocs.org/). 
The contrib folder has two templates that you can easily adapt to deploy
Mnemosyne.

Mnemosyne has two asynchronous queues that allow you to run different tasks in
parallel using a [Redis server](http://redis.io):

* **Image Queue**: when an image link is saved, Mnemosyne creates a task in the
  queue **image**. Then, a queue worker listening in this specific queue will
  download the image into memory and process it to extract the EXIF data if
  any. Once this task has been completed, the worker will create a new task in
  the following queue, passing the EXIF data (if any) as well as the link.
* **PyBossa Queue**: this queue receives the link with its EXIF data (if any).
  A worker listening in this queue, will create a PyBossa task with the link
  information for a given PyBossa application.

The queues use the [Python RQ](http://python-rq.org/) framework, so it is
really simple to setup and configure it.

## Running the web service with uwsgi

Copy the **contrib/uwsgi/mnemosyne.ini.tmpl** template, and rename it to
**mnemosyne.ini**. Then modify the values to match your paths, name, etc.

You can then run the service with the following commands (without even
activating the virtual environment):

```bash
   $ cd yourapplicationpath
   $ env/bin/uwsgi contrib/uwsgi/mnemosyne.ini
```

If the command runs successfully, you should be able to see that two sockets
are created:

* **/tmp/mnemosyne.sock**
* **/tmp/mnemosyne-stats.sock**

The first one is the web service, the second one is the uwsgi stats socket for
analyzing the performance of your setup.

## Running the queue workers

Running the queue workers is really simple. Activate the virtual environment for the
project and run the following commands for the queue **image**:

```bash
    $ cd yourapplicationpath
    $ source env/bin/activate
    $ rqworker image
```

You can repeat the same for the **pybossa** queue.

## Automating everything with Supervisord

Once you are happy with the previous configuration, use
[Supervisord](http://supervisord.org/) for running the service and the queues 
automatically (you can also use init.d scripts, it is up to you).

In the folder **contrib/supervisord** you will find three templates:

 * **mnemosyne.conf**: for the main web service
 * **mnemosyne-queue-image.conf**: for the Python RQ worker listening in the
 image queue.
 * **mnemosyne-queue-pybossa.conf**: for the Python RQ worker listening in the
 pybossa queue.

Copy them to **/etc/supervisor/conf.d/** folder (*note*: this varies from
distributions, the previous path is for Debian Ubuntu distributions), 
adapt them to fit the path for
your configuration, and restart Supervisord (or using supervisorctl reread and
update the configuration). Supervisord will create for you the log files for
all the services, and you will be able to check them at
**/var/log/supervisor/**.

Now that you have configured the web service and the queues, it is time to set
up Nginx to serve Mnemosyne on port 80.

## Deploying the server with Nginx

Copy the **contrib/nginx/mnemosyne.conf.tmpl** to **mnemosyne.conf**
file, adapt it, and place it in the nginx site folder (*note*: this varies
between distributions, in Ubuntu or Debian based ones, the folder is
*/etc/nginx/sites-available* and then a symlink into */etc/nginx/sites-enabled*
in order to enable it). Restart nginx and the service should be available.

# Deploying the service with Apache2

You need to install Apache2 and mod-wsgi to deploy the service.
In this case, we show how you can deploy it using the well known Apache2 server.

This section explains how you can install the service in an Ubuntu machine.

Install the following packages:

```bash
    $ sudo apt-get install apache2 libapache2-mod-wsgi
```

After installing the softwre, you have to enable the mod-wsgi library and
restart the web server:

```bash
    $ sudo a2enmod wsgi
    $ sudo service apache2 restart
```

Now you have to create a virtual host for hosting the micro-service. In the
**contrib/apache2** folder you can find a template that you can re-use:

```
 <VirtualHost *:80>
    ServerName example.com

    DocumentRoot /home/user/mnemosyne
    WSGIDaemonProcess mnemosyne user=user1 group=group1 threads=5
    WSGIScriptAlias / /home/user/mnemosyne/contrib/mnemosyne.wsgi

    <Directory /home/user/mnemosyne>
        WSGIProcessGroup mnemosyne
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
 </VirtualHost>
```

You can specify a user and group from your machine with lower privileges in order to 
improve the security of the site. You can also use the www-data user and group name.

Once you have adapted the PATH in that file, copy it into the folder:

 /etc/apache2/sites-available

Enable the site:

```bash
    $ sudo a2ensite mnemosyne
```

And restart the server:

```bash
    $ sudo service apache2 restart
```

The last step is to configure the queues for processing the links. In order to
do it, check the Nginx solution as it explains how you can do it.
 
Now the server is configured and up. Enjoy!
