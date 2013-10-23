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
from mnemosyne.logic.throttle import validate_ip
import json


class TestLogicThrottle(Test):
    ip = "127.0.0.1"

    def tearDown(self):
        self.db.session.remove()

    def test_00_validate_ip(self):
        """Test allow_post method"""
        with self.app.app_context():
            # Test first MAX_HITS
            for i in range(0, 5):
                err_msg = "%s st POST should be allowed" % i
                assert validate_ip(self.ip, hour=10, max_hits=5) is True, err_msg
            for i in range(0, 5):
                err_msg = "%s st POST should NOT be allowed" % i
                output = validate_ip(self.ip, hour=10, max_hits=5)
                err = json.loads(output.response[0])
                assert err['error'] == 'Rate limit reached', err_msg

            # Test if reset works
            err_msg = "Hits should be reset"
            assert validate_ip(self.ip, hour=0, max_hits=5) is True, err_msg
            # And it should be possible to post again
            for i in range(0, 4):
                err_msg = "%s st POST should be allowed" % i
                assert validate_ip(self.ip, hour=10, max_hits=5) is True, err_msg
            for i in range(0, 5):
                err_msg = "%s st POST should NOT be allowed" % i
                output = validate_ip(self.ip, hour=10, max_hits=5)
                err = json.loads(output.response[0])
                assert err['error'] == 'Rate limit reached', err_msg
