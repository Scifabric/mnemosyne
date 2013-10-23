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
    Mnemosyne
    ~~~~~~~~

    Mnemosyne logic package
"""
from flask import Response
#from urlparse import urlparse
#from mnemosyne.model.throttle import Throttle
#import datetime
import json


#def valid_link_url(url):
#    """Validate URL link"""
#    o = urlparse(url)
#    valid = ['http', 'https']
#    if (o.netloc == '') or (o.scheme not in valid):
#        return False
#    else:
#        return True


#def allow_post(ip, hour=None, max_hits=None):
#    """Manage throttling for current user"""
#    t = Throttle.query.filter_by(ip=ip).first()
#    if t:
#        now = datetime.datetime.utcnow()
#        diff = now - t.date
#
#        if hour is None:    # pragma: no cover
#            hour = 1 * 60 * 60
#
#        if max_hits is None:   # pragma: no cover
#            max_hits = 250
#        # if the IP has done a POST in the last hour, check the number of allowed hits
#        if (diff.total_seconds() < (hour)):
#            if t.hits < max_hits:
#                # Update the number hits
#                t.hits += 1
#                # Update the date
#                t.date = datetime.datetime.utcnow()
#                t.save()
#                #db.session.add(t)
#                #db.session.commit()
#                return True
#            else:
#                return False
#        else:
#            # Reset hits counter
#            t.hits = 1
#            # Update Date
#            t.date = datetime.datetime.utcnow()
#            return True
#    else:
#        t = Throttle(ip=ip, hits=1)
#        t.save()
#        #db.session.add(t)
#        #db.session.commit()
#        return True


def handle_error(error_type):
    """Return a Response with the error"""
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
        error['error'] = 'Too many arguments. url and project_slug are the only allowed arguments'
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
