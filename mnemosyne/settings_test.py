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

## DataBase URI for SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///links.db'
PORT = 5000
HOST = "0.0.0.0"

## Throttling section
# Reset counter every
HOURS = 1
# Max number of hits per HOURS
MAX_HITS = 250
# Debug for developing purposes
DEBUG = True

## PyBossa section
# Endpoint
PYBOSSA_ENDPOINT = 'http://localhost:5001'
PYBOSSA_API_KEY = 'tester'
