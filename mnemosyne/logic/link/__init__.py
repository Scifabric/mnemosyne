# -*- coding: utf-8 -*-
# This file is part of mnemosyne
#
# Copyright (C) 2013 Daniel Lombraña González
#
# Mnemosyne is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mnemosyne is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Mnemosyne. If not, see <http://www.gnu.org/licenses/>.
"""
Logic package for Link objects.

This exports:
    - validate_args a function to valide form POST args
    - save_url a function to save a link POST request
    - get_exif a function to extract EXIF data from Link.url
    - create_pybossa_task a function to create a PyBossa task for Link

"""
from flask import Response
from mnemosyne.logic import handle_error
from mnemosyne.model.link import Link
from mnemosyne.queues import q_image, q_pybossa
from StringIO import StringIO
import requests
import exifread
import json
import pbclient


def validate_args(form):
    """
    Validate form POST request arguments.

    Keyword arguments:
        form -- the form with fields url, project_slug and uri

    Return value:
        None -- if arguments are correct
        Error -- using handle_error function

    """
    if not form.get('url'):
        return handle_error('url_missing')
    if not form.get('project_slug'):
        return handle_error('project_slug_missing')
    if not form.get('uri'):
        return handle_error('uri_missing')
    if len(form.keys()) > 3:
        return handle_error('too_many_args')


def save_url(form, pybossa, project, async=True):
    """
    Save form POST request, Link, in the web service.

    Keyword arguments:
        form -- url, project_slug and uri fields to save
        pybossa -- dictionary with PyBossa api_key and endpoint value
        project -- associated Link.project
        async -- Enable/Disable async operation in queues

    Return value:
        Flask.Response -- Saved Link object in JSON format

    """
    link = Link(url=form['url'], project_id=project.id, uri=form['uri'])
    # We have a valid link, now check if this url has been already reported
    res = Link.query.filter_by(url=link.url).first()
    if res is None:
        link.status = "saved"
        link.save()
        success = dict(id=link.id,
                       url=link.url,
                       uri=link.uri,
                       new=True,
                       status=link.status)
        # Enqueue Extraction of EXIF data if not testing
        if async:
            q_image.enqueue('mnemosyne.logic.link.get_exif',
                            link.dictize(), link.project.dictize(),
                            pybossa, async)
        return Response(json.dumps(success), mimetype="application/json",
                        status=200)
    else:
        link = res
        success = dict(id=link.id,
                       url=link.url,
                       uri=link.uri,
                       new=False,
                       status=link.status)
        return Response(json.dumps(success), mimetype="application/json",
                        status=200)


def get_exif(link, project, pybossa, async=True):
    """
    Return a dictionary with the EXIF data of the image.

    Keyword arguments:
        link -- Link.dictize() object
        project -- Project.dictize() object
        pybossa -- Dictionary with PyBossa api_key and endpoint values
        async -- Enable/Disable async

    Return value:
        Link.exif -- if Link.url picture has EXIF data

    """
    from mnemosyne.core import create_app
    from mnemosyne.model.link import Link
    app = create_app()
    with app.app_context():
        r = requests.get(link['url'])
        img = StringIO(r.content)
        exif = exifread.process_file(img, details=False)
        img.close()
        tags = {}
        for k in exif.keys():
            if (('Image' in k) or ('EXIF' in k) or ('GPS' in k)):
                tags[k] = exif[k].printable
        updated_link = Link.query.get(link['id'])
        updated_link.exif = json.dumps(tags)
        updated_link.status = "img_processed"
        updated_link.save()
        # Enqueue the creation of the PyBossa task for this link if not testing
        if async:  # pragma: no cover
            q_pybossa.enqueue('mnemosyne.logic.link.create_pybossa_task',
                              link['id'], project['pb_app_short_name'],
                              pybossa)
        return updated_link.exif


def create_pybossa_task(link_id, app_short_name, pybossa):
    """
    Create a PyBossa tasks for a given app_short_name.

    Keyword arguments:
        link_id -- Link.id value
        app_short_name -- PyBossa application short_name
        pybossa -- Dictionary with PyBossa api_key and endpoint values

    Value return:
        PyBossa.task

    """
    from mnemosyne.core import create_app
    from mnemosyne.model.link import Link
    app = create_app()
    with app.app_context():
        pbclient.set('endpoint', pybossa.get('endpoint'))
        pbclient.set('api_key', pybossa.get('api_key'))
        data = pbclient.find_app(short_name=app_short_name)
        if type(data) == list and len(data) > 0:
            app = data[0]
            link = Link.query.get(link_id)
            if link.exif is None:
                link.exif = "{}"
            task_info = dict(id=link.id,
                             url=link.url,
                             project_id=link.project_id,
                             created=link.created.isoformat(),
                             exif=json.loads(link.exif))
            task = pbclient.create_task(app_id=app.id, info=task_info)
            if type(task) != dict and task.id:
                link.status = 'pybossa_task_created'
                link.pybossa_task_id = task.id
                link.save()
                return task
            else:
                link.status = 'pybossa_task_failed'
                link.save()
                return task
        else:
            return "PyBossa App %s not found" % app_short_name
