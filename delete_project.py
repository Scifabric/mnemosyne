# -*- coding: utf8 -*-
# This file is part of Mnemosyne.
#
# Copyright (C) 2013 Daniel Lombraña González

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
"""This is a program to add projects to mnemosyne with the command line."""
from optparse import OptionParser
from mnemosyne.model.project import Project
from mnemosyne.model import db
from mnemosyne.core import create_app

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-s", "--slug", dest="project_slug",
                      help="project slug NAME", metavar="STRING")

    (options, args) = parser.parse_args()

    if not options.project_slug:
        parser.error("you need to specify the project slug")

    app = create_app()
    with app.app_context():
        project = db.session.query(Project) \
                    .filter_by(slug=options.project_slug).first()
        db.session.delete(project)
        db.session.commit()
