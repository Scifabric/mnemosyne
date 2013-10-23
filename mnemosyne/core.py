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
from flask import Flask
from mnemosyne.frontend import frontend
from mnemosyne.model import db
import settings


def create_app(db_name=None, testing=False):
    app = Flask(__name__)
    app.config.from_object(settings)

    if db_name:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_name

    db.init_app(app)

    app.register_blueprint(frontend)

    return app
