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
from flask import make_response, request, current_app
from functools import update_wrapper
from model import Project, Throttle
import datetime
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
