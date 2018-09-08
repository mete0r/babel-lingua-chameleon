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
from functools import wraps
import os.path
import shutil


def isolated_directory(test_fn):
    @wraps(test_fn)
    def wrapper(self):
        name = self.id()
        cwd = os.getcwd()
        if os.path.exists(name):
            shutil.rmtree(name)
        os.makedirs(name)
        os.chdir(name)
        try:
            test_fn(self)
        finally:
            os.chdir(cwd)
    return wrapper
