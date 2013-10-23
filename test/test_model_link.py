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
from base import Test
from mnemosyne.model.link import Link
from nose.tools import raises


class TestLogicLink(Test):
    urls = [('http:', False),
            ('htt', False),
            ('ftp://example.com/img.jpg', False),
            ('http://', False),
            ('http://example.com/', True),
            ('http://example.com/img.jpg', True),
            ('data://', False)]

    def tearDown(self):
        self.db.session.remove()

    def test_00_valid_link_url(self):
        """Test Link._valid_url() method"""
        err_msg = "URL not validated correctly"
        for u in self.urls:
            l = Link(u[0], 1)
            assert l._valid_url() == u[1], err_msg

    @raises(Exception)
    def test_01_save(self):
        """Test Link.save() exception"""
        with self.app.app_context():
            l = Link("ht:pp://wrong.org/1.jpg", 1)
            l.save()
