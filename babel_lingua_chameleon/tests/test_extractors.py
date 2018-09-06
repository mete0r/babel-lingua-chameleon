# -*- coding: utf-8 -*-
#
#   babel-lingua-chameleon: Babel extractor for Chameleon templates
#   Copyright (C) 2015-2018 arbeitmachtfrei77 <arbeitmachtfrei77@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from unittest import TestCase
import io
import os.path

from ..extractors import extract_chameleon


class ExtractChameleonTest(TestCase):

    def test_extract(self):
        path = os.path.join(
            os.path.dirname(__file__),
            'fixtures',
            'html-page-template.pt',
        )
        with io.open(path, 'rb') as fp:
            keywords = ['_']
            comment_tags = []
            options = {}
            messages = extract_chameleon(fp, keywords, comment_tags, options)
            messages = list(messages)
        self.assertEquals([
            (4, None, 'page title', ['Default: Foo Bar']),
            (7, None, 'Qux', ['This is the body string']),
        ], messages)
