# This file is part of PyBossa-links.
#
# PyBossa-links is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa-links is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa-links. If not, see <http://www.gnu.org/licenses/>.

from datetime import timedelta
from flask import make_response, request, current_app, Response
from core import db, q_image, q_pybossa
from functools import update_wrapper
from model import Project, Throttle, Link
from StringIO import StringIO
import datetime
import requests
import exifread
import json
import pbclient
from urlparse import urlparse


# Based on http://flask.pocoo.org/snippets/56/
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def valid_link_url(url):
    """Validate URL link"""
    o = urlparse(url)
    if (o.netloc == '') or (o.scheme == ''):
        return False
    else:
        return True


def allow_post(db, ip, hour=None, max_hits=None):
    """Manage throttling for current user"""
    t = Throttle.query.filter_by(ip=ip).first()
    if t:
        now = datetime.datetime.utcnow()
        diff = now - t.date

        if hour is None:
            hour = 1 * 60 * 60

        if max_hits is None:
            max_hits = 250
        # if the IP has done a POST in the last hour, check the number of allowed hits
        if (diff.total_seconds() < (hour)):
            if t.hits < max_hits:
                # Update the number hits
                t.hits += 1
                # Update the date
                t.date = datetime.datetime.utcnow()
                db.session.add(t)
                db.session.commit()
                return True
            else:
                return False
        else:
            # Reset hits counter
            t.hits = 1
            # Update Date
            t.date = datetime.datetime.utcnow()
            return True
    else:
        t = Throttle(ip=ip, hits=1)
        db.session.add(t)
        db.session.commit()
        return True


def project_or_404(slug):
    """Return True if project exists, otherwise False"""
    project = Project.query.filter_by(slug=slug).first()
    if project is not None:
        return project
    else:
        return False


def handle_error(error_type):
    """Return a Response with the error"""
    error = dict(status='failed',
                 error='Something went wrong, sorry!')
    status_code = 415
    if error_type == 'invalid_url':
        error['error'] = 'Invalid URL'
    if error_type == 'url_missing':
        error['error'] = 'url arg is missing'
    if error_type == 'too_many_args':
        error['error'] = 'Too many arguments. url and project_slug are the only allowed arguments'
    if error_type == 'rate_limit':
        error['error'] = 'Rate limit reached'
    if error_type == 'project_slug_missing':
        error['error'] = 'Project slug arg is missing'
    if error_type == 'project_not_found':
        error['error'] = 'Project not found'
        status_code = 404
    if error_type == 'server_error':
        error['error'] = 'Server Error'
        status_code = 500
    print json.dumps(error)
    return Response(json.dumps(error), status_code)


def save_url(ip, form, pybossa):
        if allow_post(db=db, ip=ip,
                      hour=current_app.config.get('HOUR'),
                      max_hits=current_app.config.get('MAX_HITS')):

            if not form.get('url'):
                return handle_error('url_missing')
            if not form.get('project_slug'):
                return handle_error('project_slug_missing')
            if len(form.keys()) > 2:
                return handle_error('too_many_args')
            # First get the project
            project = Project.query.filter_by(slug=form.get('project_slug')).first()
            if project is None:
                return handle_error('project_not_found')
            if not valid_link_url(form['url']):
                return handle_error('invalid_url')
            link = Link(url=form['url'], project_id=project.id)
            # We have a valid link, now check if this url has been already reported
            res = Link.query.filter_by(url=link.url).first()
            if res is None:
                link.status = "saved"
                db.session.add(link)
                db.session.commit()
                success = dict(id=link.id,
                               url=link.url,
                               new=True,
                               status=link.status)
                # Enqueue Extraction of EXIF data
                q_image.enqueue('links.utils.get_exif',
                                link.dictize(), link.project.dictize(),
                                pybossa)
                return Response(json.dumps(success), mimetype="application/json",
                                status=200)
            else:
                link = res
                success = dict(id=link.id,
                               url=link.url,
                               new=False,
                               status=link.status)
                return Response(json.dumps(success), mimetype="application/json",
                                status=200)
        else:
            return handle_error('rate_limit')


def get_exif(link, project, pybossa):
    """Return a dictionary with the EXIF data of the image"""
    r = requests.get(link['url'])
    img = StringIO(r.content)
    exif = exifread.process_file(img, details=False)
    img.close()
    tags = {}
    for k in exif.keys():
        if (('Image' in k) or ('EXIF' in k) or ('GPS' in k)):
            tags[k] = exif[k].printable
    updated_link = db.session.query(Link).get(link['id'])
    updated_link.exif = json.dumps(tags)
    updated_link.status = "img_processed"
    db.session.commit()
    # Enqueue the creation of the PyBossa task for this link
    q_pybossa.enqueue('links.utils.create_pybossa_task',
                      link['id'], project['pb_app_short_name'], pybossa)
    return updated_link.exif


def create_pybossa_task(link_id, app_short_name, pybossa):
    """Create a PyBossa tasks for a given app_short_name"""
    pbclient.set('endpoint', pybossa.get('endpoint'))
    pbclient.set('api_key', pybossa.get('api_key'))
    data = pbclient.find_app(short_name=app_short_name)
    if type(data) == list:
        app = data[0]
        link = db.session.query(Link).get(link_id)
        task_info = dict(id=link.id,
                         url=link.url,
                         project_id=link.project_id,
                         created=link.created.isoformat(),
                         exif=json.loads(link.exif))
        task = pbclient.create_task(app_id=app.id, info=task_info)
        if task.id:
            link.status = 'pybossa_task_created'
            link.pybossa_task_id = task.id
            db.session.commit()
            return task
        else:
            link.status = 'pybossa_task_failed'
            db.session.commit()
            raise Exception
    else:
        return "PyBossa App %s not found" % app_short_name
