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

    Mnemosyne logic.throttle package
"""
from mnemosyne.model.throttle import Throttle
from mnemosyne.logic import handle_error
import datetime


def validate_ip(ip, hour=None, max_hits=None):
    """Manage throttling for current IP"""
    t = Throttle.query.filter_by(ip=ip).first()
    if t:
        now = datetime.datetime.utcnow()
        diff = now - t.date

        if hour is None:    # pragma: no cover
            hour = 1 * 60 * 60

        if max_hits is None:   # pragma: no cover
            max_hits = 250
        # if the IP has done a POST in the last hour, check the number of allowed hits
        if (diff.total_seconds() < (hour)):
            if t.hits < max_hits:
                # Update the number hits
                t.hits += 1
                # Update the date
                t.date = datetime.datetime.utcnow()
                #db.session.add(t)
                #db.session.commit()
                t._save()
                return True
            else:
                return handle_error('rate_limit')
        else:
            # Reset hits counter
            t.hits = 1
            # Update Date
            t.date = datetime.datetime.utcnow()
            t._save()
            return True
    else:
        t = Throttle(ip=ip, hits=1)
        t._save()
        return True
        #db.session.add(t)
        #db.session.commit()
