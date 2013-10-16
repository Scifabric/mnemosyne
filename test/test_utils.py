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
        """Test allow_post method"""
        ip = "127.0.0.1"
        # Test first MAX_HITS
        for i in range(0, 5):
            err_msg = "%s st POST should be allowed" % i
            assert utils.allow_post(db, ip, hour=10, max_hits=5) is True, err_msg
        for i in range(0, 5):
            err_msg = "%s st POST should NOT be allowed" % i
            assert utils.allow_post(db, ip, hour=10, max_hits=5) is False, err_msg

        # Test if reset works
        err_msg = "Hits should be reset"
        assert utils.allow_post(db, ip, hour=0, max_hits=5) is True, err_msg
        # And it should be possible to post again
        for i in range(0, 4):
            err_msg = "%s st POST should be allowed" % i
            assert utils.allow_post(db, ip, hour=10, max_hits=5) is True, err_msg
        for i in range(0, 5):
            err_msg = "%s st POST should NOT be allowed" % i
            assert utils.allow_post(db, ip, hour=10, max_hits=5) is False, err_msg

    def test_handle_error(self):
        """Test handle_error method"""
        errors = [('invalid_url', 'Invalid URL', 415),
                  ('url_missing', 'url arg is missing', 415),
                  ('too_many_args', 'Too many arguments. url and project_slug are the only allowed arguments', 415),
                  ('rate_limit', 'Rate limit reached', 415),
                  ('project_slug_missing', 'Project slug arg is missing', 415),
                  ('project_not_found', 'Project not found', 404),
                  ('server_error', 'Server Error', 500)]
        for e in errors:
            res = utils.handle_error(e[0])
            err = json.loads(res.response[0])
            assert err['status'] == 'failed', 'Member status != failed'
            assert err['error'] == e[1], "Wrong error msg for %s: %s" % (e[0],
                                                                         err['error'])
