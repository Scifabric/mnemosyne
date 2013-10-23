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
from urlparse import urlparse
import datetime


class Link(db.Model, DomainObject):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    created = db.Column(db.DateTime)
    exif = db.Column(db.Text)
    status = db.Column(db.Text)
    pybossa_task_id = db.Column(db.Integer)

    def __init__(self, url, project_id):
        self.url = url
        self.project_id = project_id
        self.created = datetime.datetime.utcnow()

    def __repr__(self):    # pragma: no cover
        return '<Link %r>' % self.url

    def _valid_url(self):
        """Validate URL link"""
        o = urlparse(self.url)
        valid = ['http', 'https']
        if (o.netloc == '') or (o.scheme not in valid):
            return False
        else:
            return True

    def save(self):
        if self._valid_url():
            self._save()
            return self
        else:
            raise Exception(u'Empty URL or invalid scheme')
