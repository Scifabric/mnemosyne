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
from flask.ext.sqlalchemy import SQLAlchemy
from redis import Redis
from rq import Queue
import settings

app = Flask(__name__)
app.config.from_object(settings)
db = SQLAlchemy(app)
# Create the Queue
q_image = Queue('image', connection=Redis())
q_pybossa = Queue('pybossa', connection=Redis())
