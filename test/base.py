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
#import pbclient
#import json
import random
from collections import namedtuple
from links.web import app
from links.core import db
from links.model import Link, Project
import tempfile

PseudoRequest = namedtuple('PseudoRequest', ['text', 'status_code', 'headers'])


class Test(object):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + tempfile.mkstemp()[1]
        print app.config['SQLALCHEMY_DATABASE_URI']
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def fixtures(self):
        # Create projects
        for i in range(0, random.randint(1, 10)):
            name = 'name_%s' % i
            slug = 'slug_%s' % i
            pb_app_short_name = 'pb_app_short_name_%s' % i
            keywords = '%s, %s, %s' % (name, slug, pb_app_short_name)
            db.session.add(Project(name, slug, pb_app_short_name, keywords))
        db.session.commit()

        # Create links
        projects = Project.query.all()
        for p in projects:
            for i in range(0, random.randint(1, 10)):
                url = 'http://%s.com/%s.jpg' % (p.slug, i)
                db.session.add(Link(url, p.id))
