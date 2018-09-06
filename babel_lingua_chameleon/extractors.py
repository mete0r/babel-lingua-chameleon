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
from __future__ import unicode_literals
from collections import namedtuple

from lingua.extractors.xml import ChameleonExtractor


Options = namedtuple('Options', [
    'domain',
    'keywords',
    'comment_tag',
])


def extract_chameleon(fileobj, keywords, comment_tags, options):
    extractor = ChameleonExtractor()

    filename = getattr(fileobj, 'name', 'unknown')
    opts = Options(
        domain=None,
        keywords=keywords,
        comment_tag=comment_tags,
    )
    for message in extractor(filename, opts, fileobj=fileobj):
        lineno = message.location[1]
        funcname = None
        msg = message.msgid
        comments = [message.comment]
        yield (lineno, funcname, msg, comments)
