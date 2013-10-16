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
from links import utils


class TestUtils(Test):
    def test_valid_link_url(self):
        """Test valid_link_url method"""
        urls = [('http:', False),
                ('htt', False),
                ('ftp://example.com/img.jpg', False),
                ('http://', False),
                ('http://example.com/', True),
                ('http://example.com/img.jpg', True),
                ('data://', False)]
        err_msg = "URL not validated correctly"
        for u in urls:
            assert utils.valid_link_url(u[0]) == u[1], err_msg

    def test_allow_post(self):
        """Test allow_post_method"""
        ip = "127.0.0.1"
        err_msg = "First POST should be allowed"
        assert utils.allow_post(db, ip, hour=10, max_hits=5) is True, err_msg
