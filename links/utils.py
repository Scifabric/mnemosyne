# This file is part of PyBossa-links.
#
# PyBossa-links is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa-links is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa-links. If not, see <http://www.gnu.org/licenses/>.

from model import Project, Throttle
import datetime
from urlparse import urlparse


def valid_link_url(url):
    """Validate URL link"""
    o = urlparse(url)
    if (o.netloc == '') or (o.scheme == ''):
        return False
    else:
        return True


def allow_post(db, ip, hour=None, max_hits=None):
    """Manage throttling for current user"""
    t = Throttle.query.filter_by(ip=ip).first()
    if t:
        now = datetime.datetime.utcnow()
        diff = now - t.date

        if hour is None:
            hour = 1 * 60 * 60

        if max_hits is None:
            max_hits = 250
        # if the IP has done a POST in the last hour, check the number of allowed hits
        if (diff.total_seconds() < (hour)):
            if t.hits < max_hits:
                # Update the number hits
                t.hits += 1
                # Update the date
                t.date = datetime.datetime.utcnow()
                db.session.add(t)
                db.session.commit()
                return True
            else:
                return False
        else:
            # Reset hits counter
            t.hits = 1
            # Update Date
            t.date = datetime.datetime.utcnow()
            return True
    else:
        t = Throttle(ip=ip, hits=1)
        db.session.add(t)
        db.session.commit()
        return True


def project_or_404(slug):
    """Return True if project exists, otherwise False"""
    project = Project.query.filter_by(slug=slug).first()
    if project is not None:
        return project
    else:
        return False
