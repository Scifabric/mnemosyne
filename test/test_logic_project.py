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
Unit Tests for logic.project package.

This exports:
    - TestLogicProject class with its unit tests

"""
import json
from base import Test
from mnemosyne.model.project import Project
from mnemosyne.logic.project import exists


class TestLogicProject(Test):

    """Class for testing logic.project package."""

    def tearDown(self):
        """Remove db.session."""
        self.db.session.remove()

    def test_00_exists(self):
        """Test exists method."""
        with self.app.app_context():
            self.project_fixtures()
            projects = Project.query.all()
            err_msg = "Project exists, however it is reporting False"
            for p in projects:
                _p = exists(slug=p.slug)
                assert _p == p, err_msg

            output = exists(slug="invented")
            err = json.loads(output.response[0])
            assert err['error'] == 'Project not found'
