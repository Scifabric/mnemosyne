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
Unit Tests for logic.throttle package.

This exports:
    - TestLogicThrottle class with its unit tests

"""
from base import Test
from mnemosyne.logic.throttle import validate_ip
import json


class TestLogicThrottle(Test):

    """Class for testing logic.throttle package."""

    ip = "127.0.0.1"

    def tearDown(self):
        """Remove db.session."""
        self.db.session.remove()

    def test_00_validate_ip(self):
        """Test allow_post method."""
        with self.app.app_context():
            # Test first MAX_HITS
            for i in range(0, 5):
                err_msg = "%s st POST should be allowed" % i
                output = validate_ip(self.ip, hour=10, max_hits=5)
                assert output is True, err_msg
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
                output = validate_ip(self.ip, hour=10, max_hits=5)
                assert output is True, err_msg
            for i in range(0, 5):
                err_msg = "%s st POST should NOT be allowed" % i
                output = validate_ip(self.ip, hour=10, max_hits=5)
                err = json.loads(output.response[0])
                assert err['error'] == 'Rate limit reached', err_msg
