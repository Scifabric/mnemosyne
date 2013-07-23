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

import json
from urlparse import urlparse
from flask import request, Response
from core import app, db
from model import Link


def handle_error(error_type):
    """Return a Response with the error"""
    error = dict(status='failed',
                 error='Something went wrong, sorry!')
    status_code = 415
    if error_type == 'invalid_url':
        error['error'] = 'Invalid URL'
    if error_type == 'url_missing':
        error['error'] = 'url field not found'
    if error_type == 'too_many_args':
        error['error'] = 'Too many arguments. url is the only allowed field'
    return Response(json.dumps(error), status_code)


@app.route("/", methods=['GET', 'POST'])
def save_url():
    if request.method == 'GET':
        links = Link.query.all()
        return "There are %s stored URLs" % len(links)
    else:
        if request.form.get('url') and (len(request.form.keys()) == 1):
            link = Link(url=request.form['url'])
            o = urlparse(link.url)
            if (o.netloc == '') or (o.scheme == ''):
                return handle_error('invalid_url')
            res = Link.query.filter_by(url=link.url).first()
            if res is None:
                db.session.add(link)
                db.session.commit()
                success = dict(id=link.id,
                               url=link.url,
                               new=True)
                return Response(json.dumps(success), 200)
            else:
                link = res
                success = dict(id=link.id,
                               url=link.url,
                               new=False)
                return Response(json.dumps(success), 200)

        else:
            if not request.form.get('url'):
                return handle_error('url_missing')
            if len(request.form.keys()) > 1:
                return handle_error('too_many_args')


if __name__ == "__main__":
    app.run()
