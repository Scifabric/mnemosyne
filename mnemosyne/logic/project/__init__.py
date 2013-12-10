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
Mnemosyne Project logic package.

This exports:
    - exists a function to check if a Project exists

"""
from mnemosyne.logic import handle_error
from mnemosyne.model.project import Project


def exists(slug):
    """
    Check if a Project exists.

    Keyword arguments:
        slug -- Project.slug name

    Return value:
        Project -- if exists
        Error -- if not found, returning an error with handle_error

    """
    project = Project.query.filter_by(slug=slug).first()
    if project:
        return project
    else:
        return handle_error('project_not_found')
