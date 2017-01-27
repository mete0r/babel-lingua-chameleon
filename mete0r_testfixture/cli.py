# -*- coding: utf-8 -*-
#
#   mete0r.testfixture: a testfixture helper
#   Copyright (C) 2015-2017 mete0r <mete0r@sarangbang.or.kr>
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
import importlib
import logging
import os.path

# PYTHON_ARGCOMPLETE_OK
try:
    import argcomplete
except ImportError:
    argcomplete = None

from . import __version__
from .testfixture import TestFixtures

logger = logging.getLogger(__name__)

locale_dir = os.path.join(os.path.dirname(__file__), 'locale')
t = gettext.translation('mete0r.testfixture', locale_dir, fallback=True)
_ = t.ugettext


def main():
    gettext.gettext = t.gettext
    parser = main_argparse()
    if argcomplete:
        argcomplete.autocomplete(parser)
    args = parser.parse_args()
    configureLogging(args.verbose)
    package = importlib.import_module(args.package)
    testfixtures = TestFixtures(package)
    testfixtures.scan()

    table = []
    for key in sorted(testfixtures.registry):
        fn = testfixtures.registry[key]
        table.append([
            ', '.join(x for x in key),
            '{}.{}'.format(fn.__module__, fn.__name__),
        ])
    try:
        from tabulate import tabulate
    except ImportError:
        for key, location in table:
            print('{}\t{}'.format(key, location))
    else:
        print(tabulate(table, headers=[
            'key',
            'location',
        ], tablefmt='grid'))


def main_argparse():
    parser = ArgumentParser()
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(__version__),
                        help=_('output version information and exit'))
    parser.add_argument('-v', '--verbose',
                        action='count',
                        help=_('increase verbosity'))
    parser.add_argument('package',
                        help=_('a python package to scan test fixtures'))
    return parser


def configureLogging(verbosity):
    if verbosity == 1:
        level = logging.INFO
    elif verbosity > 1:
        level = logging.DEBUG
    else:
        level = logging.WARNING
    try:
        import coloredlogs
    except ImportError:
        logging.basicConfig(level=level)
    else:
        coloredlogs.install(level)
