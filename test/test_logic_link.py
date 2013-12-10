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
Unit Tests for logic.link package.

This exports:
    - TestLogicLink class with its unit tests

"""
from base import Test, PseudoRequest
from mock import patch
from mnemosyne.logic.link import validate_args, save_url, get_exif, \
    create_pybossa_task
from mnemosyne.model.project import Project
from mnemosyne.model.link import Link
import json


class TestLogicLink(Test):

    """Class for testing logic.link package."""

    def tearDown(self):
        """Remove self.db.session."""
        self.db.session.remove()

    def test_01_validate_args(self):
        """Test Link.validate_args() method."""
        uri = 'http://algo.com'
        url = "%s/img.jpg" % uri
        form = dict(url=url, project_slug='slug',
                    uri=uri, extra='extra')
        res = validate_args(form)
        output = json.loads(res.response[0])
        err_msg = ('Too many arguments. url, project_slug and uri'
                   ' are the only allowed arguments')
        assert output['error'] == err_msg, output

        form.pop('extra')
        assert validate_args(form) is None, "There should not be an error"

        form = dict(project_slug='slug', uri=uri)
        res = validate_args(form)
        output = json.loads(res.response[0])
        output = json.loads(res.response[0])
        err = 'one or more arguments are missing, required: url, project_slug, uri'
        assert output['error'] == err, output

        form = dict(url=url, uri=uri)
        res = validate_args(form)
        output = json.loads(res.response[0])
        err = 'one or more arguments are missing, required: url, project_slug, uri'
        assert output['error'] == err, output

        form = dict(url=url, project_slug='slug')
        res = validate_args(form)
        output = json.loads(res.response[0])
        err = 'one or more arguments are missing, required: url, project_slug, uri'
        assert output['error'] == err, output

        form = dict(project_slug='slug')
        res = validate_args(form)
        output = json.loads(res.response[0])
        err = 'one or more arguments are missing, required: url, project_slug, uri'
        assert output['error'] == err, output

        form = dict(url=url)
        res = validate_args(form)
        output = json.loads(res.response[0])
        err = 'one or more arguments are missing, required: url, project_slug, uri'
        assert output['error'] == err, output

        form = dict(uri=uri)
        res = validate_args(form)
        output = json.loads(res.response[0])
        err = 'one or more arguments are missing, required: url, project_slug, uri'
        assert output['error'] == err, output

        form = dict()
        res = validate_args(form)
        output = json.loads(res.response[0])
        err = 'one or more arguments are missing, required: url, project_slug, uri'
        assert output['error'] == err, output

    def test_save_url(self):
        """Test save_url method."""
        with self.app.app_context():
            self.project_fixtures()
            project = Project.query.first()
            pybossa = dict(endpoint='http://pybossa.com', api_key='tester')
            form = dict(url='http://daniellombrana.es/1.jpg',
                        project_slug=project.slug,
                        uri='http://daniellombrana.es')

            res = save_url(form, pybossa, project, async=False)
            output = json.loads(res.response[0])
            err_msg = "URL should be saved"
            assert output['status'] == 'saved', err_msg
            assert output['new'] is True, err_msg

            # The same URL should be not saved, but reported as saved
            res = save_url(form, pybossa, project, async=False)
            output = json.loads(res.response[0])
            err_msg = "URL.new should be False"
            assert output['status'] == 'saved', err_msg
            assert output['new'] is False, err_msg

    def test_get_exif(self):
        """Test get_exif method."""
        with self.app.app_context():
            self.project_fixtures()
            project = Project.query.first()
            project_dict = project.dictize()
            flickr = ("http://farm3.staticflickr.com/2870/"
                      "10074898405_c31af1fc9e_o.jpg")
            link = Link(url=flickr,
                        project_id=project_dict['id'],
                        uri=flickr)
            link.save()
            pybossa = dict(endpoint='http://localhost:500', api_key='tester')
            get_exif(link.dictize(), project_dict, pybossa, async=False)
            err_msg = "The picture should have some EXIF data"
            assert link.exif is not None, err_msg

            # Now with a picture that does not have EXIF data
            flickr = ("http://farm3.staticflickr.com/2870/"
                      "10074898405_c8336bc52a_s.jpg")
            link = Link(url=flickr,
                        project_id=project_dict['id'],
                        uri=flickr)
            link.save()
            get_exif(link.dictize(), project_dict, pybossa, async=False)
            assert link.exif == "{}", "The picture should not have EXIF data"

    @patch('pbclient.requests.get')
    @patch('pbclient.requests.post')
    def test_create_pybossa_task(self, MockTask, MockApp):
        """Test create_pybossa_task method."""
        with self.app.app_context():
            self.fixtures()
            pybossa = dict(endpoint='http://localhost:5000', api_key='tester')
            short_name = 'algo'
            app = dict(id=1, short_name=short_name)
            task = dict(id=1, app_id=1)
            MockApp.return_value = PseudoRequest(text=json.dumps([app]),
                                                 status_code=200,
                                                 headers={'content-type':
                                                          'application-json'})
            MockTask.return_value = PseudoRequest(text=json.dumps(task),
                                                  status_code=200,
                                                  headers={'content-type':
                                                           'application-json'})
            link = Link.query.first()
            output = create_pybossa_task(link.id, short_name, pybossa)
            assert output.id == task['id'], "A task must be created"

            MockApp.return_value = PseudoRequest(text=json.dumps([]),
                                                 status_code=200,
                                                 headers={'content-type':
                                                          'application-json'})
            link = Link.query.first()
            output = create_pybossa_task(link.id, short_name, pybossa)
            assert output == "PyBossa App %s not found" % short_name

            task_error = dict(action="post", status="failed")
            MockApp.return_value = PseudoRequest(text=json.dumps([app]),
                                                 status_code=200,
                                                 headers={'content-type':
                                                          'application-json'})
            MockTask.return_value = PseudoRequest(text=json.dumps(task_error),
                                                  status_code=415,
                                                  headers={'content-type':
                                                           'application-json'})
            link = Link.query.first()
            output = create_pybossa_task(link.id, short_name, pybossa)
            assert output['status'] == task_error['status'], output
            assert output['action'] == task_error['action'], output
