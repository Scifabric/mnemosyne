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
from base import Test, db
from links import model


class TestPyBossaLinksLink(Test):
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
