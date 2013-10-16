# -*- coding: utf8 -*-
# This file is part of PyBossa-links.
#
# Copyright (C) 2013 Daniel Lombraña González
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
from flask import request, Response
from core import app
from utils import crossdomain, save_url
from model import Project, Link


@app.route("/", methods=['GET', 'POST'])
@crossdomain(origin='*')
def index():
    if request.method == 'GET':
        links = Link.query.all()
        projects = Project.query.all()
        return "There are %s stored URLs and %s projects" % (len(links), len(projects))
    else:
        # Check first if the user is allowed to post or if the user has reached the rate limit
        pybossa = dict(endpoint=app.config.get('PYBOSSA_ENDPOINT'),
                       api_key=app.config.get('PYBOSSA_API_KEY'))
        return save_url(request.remote_addr, request.form, pybossa,
                        hour=app.config.get('HOUR'),
                        max_hits=app.config.get('MAX_HITS'))


@app.route('/project/')
@crossdomain(origin='*')
def project():
    if (request.args.get('slug')):
        project = Project.query.filter_by(slug=request.args.get('slug')).first_or_404()
        return Response(json.dumps(project.dictize()), mimetype="application/json",
                        status=200)
    else:
        projects = Project.query.all()
        return Response(json.dumps([p.dictize() for p in projects]),
                        mimetype='application/json',
                        status=200)


if __name__ == "__main__":
    app.run(host=app.config.get('HOST'))
