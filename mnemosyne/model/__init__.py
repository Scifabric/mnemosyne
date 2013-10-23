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
    Mnemosyne
    ~~~~~~~~

    Mnemosyne model package
"""
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

    def _save(self):
        db.session.add(self)
        db.session.commit()
