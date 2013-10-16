# This file is part of PyBossa-links.
#
# Copyright (C) 2013 Daniel Lombraña González

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
from optparse import OptionParser
from links.model import Project
from links.core import db

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-n", "--name", dest="project_name",
                      help="project NAME", metavar="STRING")
    parser.add_option("-s", "--slug", dest="project_slug",
                      help="project slug NAME", metavar="STRING")
    parser.add_option("-k", "--keywords", dest="project_keywords",
                      help="project KEYWORDS (comma separated)", metavar="STRING")
    parser.add_option("-p", "--pybossa", dest="pb_app_short_name",
                      help="PyBossa app short_name", metavar="STRING")

    (options, args) = parser.parse_args()

    if not options.project_name:
        parser.error("you need to specify the project name")

    if not options.project_slug:
        parser.error("you need to specify the project slug")

    if not options.project_keywords:
        parser.error("you need to specify the project keywords")

    if not options.pb_app_short_name:
        parser.error("you need to specify the PyBossa app short_name")

    project = Project(name=options.project_name,
                      slug=options.project_slug,
                      pb_app_short_name=options.pb_app_short_name,
                      keywords=options.project_keywords.strip())
    db.session.add(project)
    db.session.commit()
