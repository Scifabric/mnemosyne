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
Unit Tests for Logic package.

This exports:
    - TestLogic class for running the tests

"""
from base import Test
from mnemosyne.logic import handle_error
import json


class TestLogic(Test):

    """Class for testing Logic package."""

    def test_handle_error(self):
        """Test handle_error method."""
        errors = [('invalid_url', 'Invalid URL', 415),
                  ('url_missing', 'url arg is missing', 415),
                  ('too_many_args', 'Too many arguments. '
                                    'url and project_slug are '
                                    'the only allowed arguments', 415),
                  ('rate_limit', 'Rate limit reached', 415),
                  ('project_slug_missing', 'project_slug arg is missing', 415),
                  ('project_not_found', 'Project not found', 404),
                  ('server_error', 'Server Error', 500),
                  ('unknown', 'Server Error', 500)]
        for e in errors:
            res = handle_error(e[0])
            err = json.loads(res.response[0])
            assert err['status'] == 'failed', 'Member status != failed'
            err_msg = "Wrong error msg for %s: %s" % (e[0], err['error'])
            assert err['error'] == e[1], err_msg
