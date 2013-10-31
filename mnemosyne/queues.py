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
Package for creating Mnemosyne Python-RQ queues.

This exports:
    - setup_queues a function that creates two queues: q_image and q_pybossa

"""
from redis import Redis
from rq import Queue


def setup_queues(async=True):
    """
    Configure Python-RQ queues for mnemosyne.

    Keyword arguments:
        async -- Enable/Disable async jobs

    Return value:
        q_image -- Python-RQ queue for processing image links
        q_pybossa -- Python-RQ queue for creating PyBossa tasks

    """
    _q_image = Queue('image', connection=Redis(), async=async)
    _q_pybossa = Queue('pybossa', connection=Redis(), async=async)
    return _q_image, _q_pybossa

q_image, q_pybossa = setup_queues()
