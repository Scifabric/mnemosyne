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
from flask import request, Response, abort
from core import app, db
from utils import allow_post, valid_link_url
from model import Project, Link


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
    return Response(json.dumps(error), status_code)


@app.route("/", methods=['GET', 'POST'])
def save_url():
    if request.method == 'GET':
        links = Link.query.all()
        projects = Project.query.all()
        return "There are %s stored URLs and %s projects" % (len(links), len(projects))
    else:
        # Check first if the user is allowed to post or he has reached the rate limit
        if allow_post(db=db, ip=request.remote_addr,
                      hour=app.config.get('HOUR'),
                      max_hits=app.config.get('MAX_HITS')):

            if not request.form.get('url'):
                return handle_error('url_missing')
            if not request.form.get('project_slug'):
                return handle_error('project_slug_missing')
            if len(request.form.keys()) > 2:
                return handle_error('too_many_args')
            # First get the project
            project = Project.query.filter_by(slug=request.form.get('project_slug')).first()
            if project is None:
                return handle_error('project_not_found')
            if not valid_link_url(request.form['url']):
                return handle_error('invalid_url')
            link = Link(url=request.form['url'], project_id=project.id)
            # We have a valid link, now check if this url has been already reported
            res = Link.query.filter_by(url=link.url).first()
            if res is None:
                db.session.add(link)
                db.session.commit()
                success = dict(id=link.id,
                               url=link.url,
                               new=True,
                               status="success")
                return Response(json.dumps(success), 200)
            else:
                link = res
                success = dict(id=link.id,
                               url=link.url,
                               new=False,
                               status="success")
                return Response(json.dumps(success), 200)
        else:
            return handle_error('rate_limit')


@app.route('/project/')
def projects():
    if (request.args.get('slug')):
        project = Project.query.filter_by(slug=request.args.get('slug')).first()
        if project:
            links = Link.query.filter_by(project_id=project.id).count()
            return ("Project %s has %s stored links for the following keywords: %s"
                    % (project.name, links, project.keywords))
        else:
            return abort(404)
    else:
        projects = Project.query.count()
        return "There are %s registered projects" % projects


if __name__ == "__main__":
    app.run()
