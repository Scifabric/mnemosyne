# -*- coding: utf8 -*-
# This file is part of Mnemosyne.
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
Tests for Link logic and model.

This exports:
    - TestLinks class for testing Mnemosyne Link object and logic

"""
import json
from base import Test
from mnemosyne.model.link import Link
from mnemosyne.model.project import Project


class TestLinks(Test):

    """Class for testing Link logic and objects."""

    def test_00_GET_index(self):
        """Test GET INDEX web page."""
        # With nothing on the DB
        res = self.tc.get('/')
        msg = "There are 0 stored URLs and 0 projects"
        assert msg == res.data, "There should be 0 stored URLs and projects"

        # With some links and projects
        with self.app.app_context():
            self.fixtures()
            n_projects = Project.query.count()
            n_links = Link.query.count()
            res = self.tc.get('/')
            msg = "There are %s stored URLs and %s projects" % (n_links,
                                                                n_projects)
            err_msg = ("There should be %s stored URLs and %s projects"
                       % (n_links, n_projects))
            assert msg == res.data, err_msg

    def test_POST_index(self):
        """Test POST INDEX web page."""
        with self.app.app_context():
            self.fixtures()
            project = Project.query.first()
            link = {'url': 'http://new.com/img.jpg',
                    'project_slug': project.slug}
            res = self.tc.post('/', data=link)
            status = json.loads(res.data)
            assert status['status'] == 'saved', status
            assert status['new'] is True, status
            assert status['id'] is not None, status

            # If the same link is reported posted twice:
            res = self.tc.post('/', data=link)
            status = json.loads(res.data)
            assert status['status'] == 'saved', status
            assert status['new'] is False, status
            assert status['id'] is not None, status

    def test_GET_project(self):
        """Test GET PROJECT web page."""
        # Empty DB
        with self.app.app_context():
            res = self.tc.get('/project/')
            output = json.loads(res.data)
            assert len(output) == 0, "It should return an empty list"

            # Now with some data
            self.fixtures()
            projects = Project.query.all()
            res = self.tc.get('/project/')
            output = json.loads(res.data)
            err_msg = "There should be the same number of projects"
            assert len(output) == len(projects), err_msg
            for p in projects:
                assert p.dictize() in output, "A project is missing"

            # Get a specific project
            res = self.tc.get('/project/?slug=%s' % projects[0].slug)
            output = json.loads(res.data)
            err_msg = "The returned project is wrong"
            assert output["id"] == projects[0].id, err_msg
            assert res.status_code == 200, self.ERR_MSG_200_STATUS_CODE

            # Get a project that does not exist
            res = self.tc.get('/project/?slug=inventado')
            assert res.status_code == 404, self.ERR_MSG_404_STATUS_CODE
