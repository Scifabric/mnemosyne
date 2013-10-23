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
from mnemosyne.model import DomainObject, db
import datetime


class Throttle(db.Model, DomainObject):
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

    def __repr__(self):    # pragma: no cover
        return '<Throttle %r:%r>' % (self.ip, self.hits)
