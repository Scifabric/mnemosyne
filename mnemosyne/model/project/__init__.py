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
Model for Project object.

This exports:
    - Project a class for creating/managing/storing Project objects

"""
from mnemosyne.model import DomainObject, db
import datetime


class Project(db.Model, DomainObject):

    """
    Class for Project object.

    Keyword arguments:
        name -- Project name
        slug -- Project short name or slug
        pb_app_short_name -- PyBossa application short_name related to project
        keywords -- Project keywords

    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    slug = db.Column(db.String(50), unique=True)
    pb_app_short_name = db.Column(db.String(255), unique=True)
    keywords = db.Column(db.Text)
    created = db.Column(db.DateTime)

    # Relations: one to many
    links = db.relationship('Link', cascade="all, delete", backref='project', lazy='dynamic')

    def __init__(self, name, slug, pb_app_short_name, keywords):
        self.name = name
        self.slug = slug
        self.pb_app_short_name = pb_app_short_name
        self.keywords = keywords
        self.created = datetime.datetime.utcnow()

    def __repr__(self):    # pragma: no cover
        return '<Project %r:%r>' % (self.slug, self.id)
