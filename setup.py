# -*- coding: utf-8 -*-
#
#   METE0R-PROJECT: SOME_DESCRIPTION
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
from __future__ import with_statement
from contextlib import contextmanager
from distutils.command.build import build as _build
import io
import os.path


def setup_dir(f):
    ''' Decorate f to run inside the directory where setup.py resides.
    '''
    setup_dir = os.path.dirname(os.path.abspath(__file__))

    def wrapped(*args, **kwargs):
        with chdir(setup_dir):
            return f(*args, **kwargs)

    return wrapped


@contextmanager
def chdir(new_dir):
    old_dir = os.path.abspath(os.curdir)
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(old_dir)


@setup_dir
def import_setuptools():
    try:
        import setuptools
        return setuptools
    except ImportError:
        pass

    import ez_setup
    ez_setup.use_setuptools()
    import setuptools
    return setuptools


@setup_dir
def readfile(path):
    with io.open(path, encoding='utf-8') as f:
        return f.read()


@setup_dir
def get_version():
    from METE0R_PACKAGE import __version__
    return __version__


def alltests():
    import sys
    import unittest
    import zope.testrunner.find
    import zope.testrunner.options
    here = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    args = sys.argv[:]
    defaults = ['--test-path', here]
    options = zope.testrunner.options.get_options(args, defaults)
    suites = list(zope.testrunner.find.find_suites(options))
    return unittest.TestSuite(suites)


install_requires_filename = 'requirements-app.in'
install_requires = readfile(install_requires_filename)

tests_require = readfile('requirements-test.in')


setup_info = {
    'name': 'METE0R-PROJECT',
    'version': get_version(),
    'description': 'SOME_DESCRIPTION',
    'long_description': '\n'.join([readfile('README.rst'),
                                   readfile('CHANGES.rst')]),

    'author': 'mete0r',
    'author_email': 'mete0r@sarangbang.or.kr',
    'license': 'GNU Affero General Public License v3 or later (AGPLv3+)',
    # 'url': 'https://github.com/mete0r/METE0R-PROJECT',

    'packages': [
        'METE0R_PACKAGE',
        'METE0R_PACKAGE.recipe',
        'METE0R_PACKAGE.tests',
    ],
    # do not use '.'; just omit to specify setup.py directory
    'package_dir': {
        # '': 'src',
    },
    'package_data': {
        'METE0R_PACKAGE': [
            'locale/*/*/*.mo',
        ],
        # 'METE0R_PACKAGE.tests': [
        #   'files/*',
        # ],
    },
    'install_requires': install_requires,
    'test_suite': '__main__.alltests',
    'tests_require': tests_require,
    'extras_require': {
        'test': tests_require,
    },
    'setup_requires': [
        'babel',
        'mete0r.distutils.virtualenv == 0.0.2',
    ],
    'message_extractors': {
        'METE0R_PACKAGE': [
            ('**.py', 'python', None),
        ]
    },
    'entry_points': {
        'console_scripts': [
            'METE0R_PACKAGE = METE0R_PACKAGE.cli:main',
        ],
        'zc.buildout': [
            'default = METE0R_PACKAGE.recipe:Recipe',
        ],
        'zc.buildout.uninstall': [
            'default = METE0R_PACKAGE.recipe:uninstall',
        ],
        'paste.app_factory': [
            'main = METE0R_PACKAGE.wsgi:app_factory',
        ],
    },
    'classifiers': [
        # 'Development Status :: 4 - Beta',
        # 'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',  # noqa
        # 'Operating System :: OS Independent',
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: Implementation :: CPython',
    ],
    'keywords': [
    ],
    'zip_safe': False,
}


class build(_build):
    def run(self):
        self.run_command('compile_catalog')
        _build.run(self)


project_root_directory = os.path.abspath(os.path.dirname(__file__))
requirements_path = 'requirements.txt'


@setup_dir
def main():
    setuptools = import_setuptools()
    setup_info['cmdclass'] = {
        'build': build,
    }
    setuptools.setup(**setup_info)


if __name__ == '__main__':
    main()
