# -*- coding: utf8 -*-
# This file is part of PyBossa-links.
#
# Copyright (C) 2013 Daniel Lombraña González
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import json
from base import Test, db, PseudoRequest
from links import utils, model
from mock import patch


class TestUtils(Test):

    def tearDown(self):
        db.session.remove()

    def test_valid_link_url(self):
        """Test valid_link_url method"""
        urls = [('http:', False),
                ('htt', False),
                ('ftp://example.com/img.jpg', False),
                ('http://', False),
                ('http://example.com/', True),
                ('http://example.com/img.jpg', True),
                ('data://', False)]
        err_msg = "URL not validated correctly"
        for u in urls:
            assert utils.valid_link_url(u[0]) == u[1], err_msg

    def test_allow_post(self):
        """Test allow_post method"""
        ip = "127.0.0.1"
        # Test first MAX_HITS
        for i in range(0, 5):
            err_msg = "%s st POST should be allowed" % i
            assert utils.allow_post(db, ip, hour=10, max_hits=5) is True, err_msg
        for i in range(0, 5):
            err_msg = "%s st POST should NOT be allowed" % i
            assert utils.allow_post(db, ip, hour=10, max_hits=5) is False, err_msg

        # Test if reset works
        err_msg = "Hits should be reset"
        assert utils.allow_post(db, ip, hour=0, max_hits=5) is True, err_msg
        # And it should be possible to post again
        for i in range(0, 4):
            err_msg = "%s st POST should be allowed" % i
            assert utils.allow_post(db, ip, hour=10, max_hits=5) is True, err_msg
        for i in range(0, 5):
            err_msg = "%s st POST should NOT be allowed" % i
            assert utils.allow_post(db, ip, hour=10, max_hits=5) is False, err_msg

    def test_handle_error(self):
        """Test handle_error method"""
        errors = [('invalid_url', 'Invalid URL', 415),
                  ('url_missing', 'url arg is missing', 415),
                  ('too_many_args', 'Too many arguments. url and project_slug are the only allowed arguments', 415),
                  ('rate_limit', 'Rate limit reached', 415),
                  ('project_slug_missing', 'project_slug arg is missing', 415),
                  ('project_not_found', 'Project not found', 404),
                  ('server_error', 'Server Error', 500),
                  ('unknown', 'Server Error', 500)]
        for e in errors:
            res = utils.handle_error(e[0])
            err = json.loads(res.response[0])
            assert err['status'] == 'failed', 'Member status != failed'
            assert err['error'] == e[1], "Wrong error msg for %s: %s" % (e[0],
                                                                         err['error'])

    def test_validate_post_args(self):
        """Test validate_post_args method"""
        form = dict(url='http://algo', project_slug='slug', extra='extra')
        res = utils.validate_post_args(form)
        output = json.loads(res.response[0])
        assert output['error'] == 'Too many arguments. url and project_slug are the only allowed arguments', output

        form.pop('extra')
        assert utils.validate_post_args(form) is None, "There should not be an error"

        form = dict(project_slug='slug')
        res = utils.validate_post_args(form)
        output = json.loads(res.response[0])
        assert output['error'] == 'url arg is missing', output

        form = dict(url='http://algo')
        res = utils.validate_post_args(form)
        output = json.loads(res.response[0])
        assert output['error'] == 'project_slug arg is missing', output

    def test_save_url(self):
        """Test save_url method"""
        self.project_fixtures()
        project = db.session.query(model.Project).first()
        pybossa = dict(endpoint='http://pybossa.com', api_key='tester')
        form = dict(url='http://daniellombrana.es', project_slug=project.slug)

        # Save without taking care of Throttling
        res = utils.save_url("127.0.0.1", form, pybossa, hour=0, max_hits=2)
        output = json.loads(res.response[0])
        err_msg = "URL should be saved"
        assert output['status'] == 'saved', err_msg
        assert output['new'] is True, err_msg

        # The same URL should be not saved, but reported
        res = utils.save_url("127.0.0.1", form, pybossa, hour=1000, max_hits=2)
        output = json.loads(res.response[0])
        err_msg = "URL.new should be False"
        assert output['status'] == 'saved', err_msg
        assert output['new'] is False, err_msg

        # With Throttling
        res = utils.save_url("127.0.0.1", form, pybossa, hour=1000, max_hits=2)
        output = json.loads(res.response[0])
        print output
        err_msg = "It should not allow to save the link"
        assert output['status'] == 'failed', err_msg

    def test_get_exif(self):
        """Test get_exif method"""
        self.project_fixtures()
        project = db.session.query(model.Project).first()
        link = model.Link(url="http://farm3.staticflickr.com/2870/10074898405_c31af1fc9e_o.jpg",
                          project_id=project.id)
        db.session.add(link)
        db.session.commit()
        pybossa = dict(endpoint='http://localhost:500', api_key='tester')
        utils.get_exif(link.dictize(), project.dictize(), pybossa)
        assert link.exif is not None, "The picture should have some EXIF data"

        # Now with a picture that does not have EXIF data
        link = model.Link(url="http://farm3.staticflickr.com/2870/10074898405_c8336bc52a_s.jpg",
                          project_id=project.id)
        db.session.add(link)
        db.session.commit()
        utils.get_exif(link.dictize(), project.dictize(), pybossa)
        assert link.exif == "{}", "The picture should not have EXIF data"

    @patch('pbclient.requests.get')
    @patch('pbclient.requests.post')
    def test_create_pybossa_task(self, MockTask, MockApp):
        """Test create_pybossa_task method"""
        self.fixtures()
        pybossa = dict(endpoint='http://localhost:500', api_key='tester')
        short_name = 'algo'
        app = dict(id=1, short_name=short_name)
        task = dict(id=1, app_id=1)
        MockApp.return_value = PseudoRequest(text=json.dumps([app]), status_code=200, headers={'content-type': 'application-json'})
        MockTask.return_value = PseudoRequest(text=json.dumps(task), status_code=200, headers={'content-type': 'application-json'})
        output = utils.create_pybossa_task(1, short_name, pybossa)
        assert output.id == task['id'], "A task must be created"

        MockApp.return_value = PseudoRequest(text=json.dumps([]), status_code=200, headers={'content-type': 'application-json'})
        output = utils.create_pybossa_task(1, short_name, pybossa)
        assert output == "PyBossa App %s not found" % short_name

        task_error = dict(action="post", status="failed")
        MockApp.return_value = PseudoRequest(text=json.dumps([app]), status_code=200, headers={'content-type': 'application-json'})
        MockTask.return_value = PseudoRequest(text=json.dumps(task_error), status_code=415, headers={'content-type': 'application-json'})
        output = utils.create_pybossa_task(1, short_name, pybossa)
        assert output['status'] == task_error['status'], output
        assert output['action'] == task_error['action'], output
