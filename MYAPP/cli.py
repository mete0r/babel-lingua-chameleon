# -*- coding: utf-8 -*-
#
#   MYAPP : SOME_DESCRIPTION
#   Copyright (C) 2015 mete0r <mete0r@sarangbang.or.kr>
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
from argparse import ArgumentParser
import gettext
import os.path

from . import __version__

locale_dir = os.path.join(os.path.dirname(__file__), 'locale')
t = gettext.translation('MYAPP', locale_dir, fallback=True)
_ = t.ugettext


def main():
    gettext.gettext = t.gettext
    parser = ArgumentParser()
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(__version__),
                        help=_('output version information and exit'))
    args = parser.parse_args()
    args
