# -*- coding: utf8 -*-
# This file is part of PyBossa-links.
#
# Copyright (C) 2013 Daniel Lombraña González
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


class DomainObject(object):
    def dictize(self):
        tmp = {}
        for col in self.__table__.c:
            if col.name == 'created':
                tmp[col.name] = getattr(self, col.name).isoformat()
            elif col.name == 'keywords':
                tmp[col.name] = [k.strip() for k in getattr(self, col.name).split(",")]
            else:
                tmp[col.name] = getattr(self, col.name)
        return tmp


class Project(db.Model, DomainObject):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    slug = db.Column(db.String(50), unique=True)
    pb_app_short_name = db.Column(db.String(255), unique=True)
    keywords = db.Column(db.Text)
    created = db.Column(db.DateTime)

    # Relations: one to many
    links = db.relationship('Link', backref='project', lazy='dynamic')

    def __init__(self, name, slug, pb_app_short_name, keywords):
        self.name = name
        self.slug = slug
        self.pb_app_short_name = pb_app_short_name
        self.keywords = keywords
        self.created = datetime.datetime.utcnow()

    def __repr__(self):    # pragma: no cover
        return '<Project %r:%r>' % (self.slug, self.id)


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
