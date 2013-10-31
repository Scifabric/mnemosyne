# -*- coding: utf8 -*-
# This file is part of Mnemosyne
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
A Flask web application for storing links and create PyBossa tasks.

This package allows you to collect image links, submitted in a POST request.

This exports:
    - mnemosyne.logic is a package to handle the logic of storing links
    - mnemosyne.model is the database model package for the web service
    - mnemosyne.views is a package with the frontend view
    - mnemosyne.core is the package to create the web app (create_app)
    - mnemosyne.frontend is the Flask.Blueprint for the front end
    - mnemosyne.queues is the package to create Python-RD queues
    - mnemosyne.settings is the package with the configuration
    - mnemosyne.utils is the package that exports crossdomain function

"""
