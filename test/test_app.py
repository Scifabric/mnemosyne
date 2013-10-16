# -*- coding: utf8 -*-
# This file is part of PyBossa-links.
#
# Copyright (C) 2013 Daniel Lombraña González
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import json
from base import Test, db
from links import model


class TestLinks(Test):
    def test_GET_index(self):
        """Test GET INDEX web page"""
        # With nothing on the DB
        res = self.app.get('/')
        msg = "There are 0 stored URLs and 0 projects"
        assert msg == res.data, "There should be 0 stored URLs and projects"

        # With some links and projects
        self.fixtures()
        n_projects = db.session.query(model.Project).count()
        n_links = db.session.query(model.Link).count()
        res = self.app.get('/')
        msg = "There are %s stored URLs and %s projects" % (n_links, n_projects)
        err_msg = "There should be %s stored URLs and %s projects" % (n_links,
                                                                      n_projects)
        assert msg == res.data, err_msg

    def test_POST_index(self):
        """Test POST INDEX web page"""
        self.fixtures()
        project = db.session.query(model.Project).first()
        link = {'url': 'http://new.com/img.jpg', 'project_slug': project.slug}
        res = self.app.post('/', data=link)
        status = json.loads(res.data)
        assert status['status'] == 'saved', status
        assert status['new'] is True, status
        assert status['id'] is not None, status

        # If the same link is reported posted twice:
        res = self.app.post('/', data=link)
        status = json.loads(res.data)
        assert status['status'] == 'saved', status
        assert status['new'] is False, status
        assert status['id'] is not None, status

    def test_GET_project(self):
        """Test GET PROJECT web page"""
        # Empty DB
        res = self.app.get('/project/')
        output = json.loads(res.data)
        assert len(output) == 0, "It should return an empty list"

        # Now with some data
        self.fixtures()
        projects = db.session.query(model.Project).all()
        res = self.app.get('/project/')
        output = json.loads(res.data)
        err_msg = "There should be the same number of projects"
        assert len(output) == len(projects), err_msg
        for p in projects:
            assert p.dictize() in output, "A project is missing"

        # Get a specific project
        res = self.app.get('/project/?slug=%s' % projects[0].slug)
        output = json.loads(res.data)
        assert output["id"] == projects[0].id, "The returned project is wrong"
        assert res.status_code == 200, self.ERR_MSG_200_STATUS_CODE

        # Get a project that does not exist
        res = self.app.get('/project/?slug=inventado')
        assert res.status_code == 404, self.ERR_MSG_404_STATUS_CODE
