# -*- coding: utf-8 -*-
#
#   mete0r_testfixture: a testfixture helper
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
import logging

import venusian


logger = logging.getLogger(__name__)


class TestFixtures(object):

    def __init__(self, package):
        self.package = package
        self.scanned = False
        self.registry = {}

    def scan(self):
        if self.scanned:
            return
        scanner = venusian.Scanner(testfixtures=self)
        scanner.scan(self.package, categories=('testfixture',))

    def get(self, *args):
        if not self.scanned:
            self.scan()
        fn = self.registry[args]
        return fn(self)


def testfixture(*args):
    def decorator(wrapped):
        def callback(scanner, name, ob):
            try:
                testfixtures = scanner.testfixtures
            except AttributeError:
                return
            logger.debug(
                'scanned %s.%s as %r',
                ob.__module__,
                ob.__name__,
                args
            )
            testfixtures.registry[args] = ob
        venusian.attach(wrapped, callback, category='testfixture')
        return wrapped
    return decorator
