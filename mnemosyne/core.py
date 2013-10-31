# -*- coding: utf8 -*-
# This file is part of Mnemosyne.
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
Package for creating the Flask application.

This exports:
    - create_app a function that creates the Flask application

"""
from flask import Flask
from mnemosyne.frontend import frontend
from mnemosyne.model import db
import mnemosyne.settings as settings


def create_app(db_name=None, testing=False):
    """
    Create the Flask app object after configuring it.

    Keyword arguments:
        db_name -- Database name
        testing -- Enable/Disable testing mode

    Return value:
        app -- Flask application object

    """
    app = Flask(__name__)
    app.config.from_object(settings)

    if db_name:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_name

    db.init_app(app)

    app.register_blueprint(frontend)

    return app
