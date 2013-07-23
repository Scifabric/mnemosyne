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
from core import db
import datetime


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '<Link %r>' % self.url


class Throttle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Request IP: origin of the API request
    ip = db.Column(db.Text, unique=True)
    # Number of times that the IP has hitten the API
    hits = db.Column(db.Integer)
    # DateTime of last hit
    date = db.Column(db.DateTime)

    def __init__(self, ip, hits):
        self.ip = ip
        self.hits = hits
        self.date = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Throttle %r:%r>' % (self.ip, self.hits)
