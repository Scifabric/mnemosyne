# -*- coding: utf-8 -*-
# This file is part of mnemosyne
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
Mnemosyne logic package.

This exports:
    - logic.link subpacakge
    - logic.project subpackage
    - logic.throttle subpacakge
    - handle_error a function to handle the app errors

"""
from flask import Response
import json


def handle_error(error_type):
    """
    Return a Response with the error in JSON format.

    Keyword arguments:
        error_type -- String representing the error

    Return value:
        Flask.Response -- In JSON format representing the error

    """
    error = dict(status='failed',
                 error='Server Error')
    status_code = 500
    if error_type == 'invalid_url':
        error['error'] = 'Invalid URL'
        status_code = 415
    if error_type == 'url_missing':
        error['error'] = 'url arg is missing'
        status_code = 415
    if error_type == 'too_many_args':
        error['error'] = "Too many arguments. url and project_slug \
                          are the only allowed arguments"
        status_code = 415
    if error_type == 'rate_limit':
        error['error'] = 'Rate limit reached'
        status_code = 415
    if error_type == 'project_slug_missing':
        error['error'] = 'project_slug arg is missing'
        status_code = 415
    if error_type == 'project_not_found':
        error['error'] = 'Project not found'
        status_code = 404
    if error_type == 'server_error':
        error['error'] = 'Server Error'
        status_code = 500
    return Response(json.dumps(error), status_code)
