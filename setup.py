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
from __future__ import with_statement
from contextlib import contextmanager
from distutils.cmd import Command
from distutils.command.build import build as _build
from subprocess import check_call
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
    from MYAPP import __version__
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
    'name': 'MYAPP',
    'version': get_version(),
    'description': 'SOME_DESCRIPTION',
    'long_description': '\n'.join([readfile('README.rst'),
                                   readfile('CHANGES.rst')]),

    'author': 'mete0r',
    'author_email': 'mete0r@sarangbang.or.kr',
    'license': 'GNU Affero General Public License v3 or later (AGPLv3+)',
    # 'url': 'https://github.com/mete0r/MYAPP',

    'packages': [
        'MYAPP',
        'MYAPP.recipe',
        'MYAPP.tests',
    ],
    # do not use '.'; just omit to specify setup.py directory
    'package_dir': {
        # '': 'src',
    },
    'package_data': {
        'MYAPP': [
            'locale/*/*/*.mo',
        ],
        # 'MYAPP.tests': [
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
        'virtualenv >= 15.0.3',
    ],
    'message_extractors': {
        'MYAPP': [
            ('**.py', 'python', None),
        ]
    },
    'entry_points': {
        'console_scripts': [
            'MYAPP = MYAPP.cli:main',
        ],
        'zc.buildout': [
            'default = MYAPP.recipe:Recipe',
        ],
        'zc.buildout.uninstall': [
            'default = MYAPP.recipe:uninstall',
        ],
        'paste.app_factory': [
            'main = MYAPP.wsgi:app_factory',
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


class virtualenv(Command):

    description = 'create a virtualenv environement'

    user_options = [
        (
            'venv-directory=', 'd',
            'venv directory [default: %s]' % project_root_directory,
        )
    ]

    def initialize_options(self):
        self.venv_directory = project_root_directory
        self.bin_dir = None

    def finalize_options(self):
        if self.venv_directory.startswith('/'):
            self.venv_directory = self.venv_directory
        else:
            self.venv_directory = os.path.abspath(
                os.path.join(
                    project_root_directory,
                    self.venv_directory,
                ),
            )
        import virtualenv
        home_dir, lib_dir, inc_dir, bin_dir = virtualenv.path_locations(
            self.venv_directory
        )
        self.bin_dir = bin_dir

    def run(self):
        import virtualenv
        self.execute(
            virtualenv.create_environment,
            tuple([self.venv_directory]),
        )
        self.pip_install([
            'setuptools',
            'pip',
            'pip-tools>=1.7.0',
        ], upgrade=True)

    def pip_install(self, requirements, upgrade=False):
        pip = os.path.join(self.bin_dir, 'pip')
        cmd = [
            pip, 'install',
        ]
        if upgrade:
            cmd.append('-U')
        cmd.extend(requirements)
        self.execute(
            check_call,
            tuple([cmd]),
        )

    def pip_wheel(self, requirements, output_directory):
        pip = os.path.join(self.bin_dir, 'pip')
        cmd = [
            pip, 'wheel',
        ]
        cmd.extend(requirements)
        cmd.extend([
            '-w', output_directory,
        ])
        self.execute(
            check_call,
            tuple([cmd]),
        )

    def pip_sync(self, requirements, find_links=(), no_index=False):
        pip_sync = os.path.join(self.bin_dir, 'pip-sync')
        cmd = [
            pip_sync,
        ]
        if self.dry_run:
            cmd.extend([
                '--dry-run',
            ])
        for find_link in find_links:
            cmd.extend([
                '-f', find_link
            ])
        if no_index:
            cmd.append('--no-index')
        cmd.append(requirements)
        self.announce('check_call(%r)' % cmd)
        check_call(cmd)

    def pip_compile(self, output_file, requirements, find_links=(),
                    no_index=False, upgrade=False):
        pip_compile = os.path.join(self.bin_dir, 'pip-compile')
        cmd = [
            pip_compile, '-o', output_file,
        ]
        if self.dry_run:
            cmd.extend([
                '--dry-run',
            ])
        for find_link in find_links:
            cmd.extend([
                '-f', find_link
            ])
        if no_index:
            cmd.append('--no-index')
        if upgrade:
            cmd.append('--upgrade')
        cmd.extend(requirements)
        self.announce('check_call(%r)' % cmd)
        check_call(cmd)

    subcommands = [
    ]


class virtualenv_bootstrap_script(Command):

    description = 'generate virtualenv bootstrap script (experimental)'

    bootstrap_script_filename = 'bootstrap-virtualenv.py'

    user_options = [
        (
            'requirement=', 'r',
            'requirements file [default: %s]' % requirements_path
        ), (
            'output-file=', 'o',
            'output file [default: %s]' % bootstrap_script_filename
        )
    ]

    def initialize_options(self):
        self.output_file = self.bootstrap_script_filename
        self.requirement = requirements_path
        self.virtualenv_support = 'virtualenv_support'

    def finalize_options(self):
        pass

    def run(self):
        import virtualenv
        extra_text = readfile('bootstrap-virtualenv.in')
        script = virtualenv.create_bootstrap_script(
            extra_text,
        )
        with io.open(self.output_file, 'w') as f:
            f.write(script)

        virtualenv_command = self.get_finalized_command('virtualenv')
        virtualenv_command.pip_wheel(
            ['setuptools', 'pip', 'wheel', 'pip-tools>=1.7.0'],
            self.virtualenv_support,
        )
        virtualenv_command.pip_wheel(
            ['-r', self.requirement],
            self.virtualenv_support,
        )


class pip_sync(Command):

    description = \
            'synchronize a virtualenv with the requirements specification.'

    user_options = [
        (
            'requirement=', 'r',
            'requirements file [default: %s]' % requirements_path
        ), (
            'find-links=', 'f',
            'Look for archives in this directory or on this HTML page'
        ), (
            'no-index', None,
            'Add index URL to generated file',
        )
    ]

    def initialize_options(self):
        self.find_links = None
        self.no_index = 0
        self.requirement = requirements_path

    def finalize_options(self):
        self.ensure_string_list('find_links')
        self.find_links = self.find_links or ()
        self.find_links = filter(lambda x: x, self.find_links)
        self.dump_options()

    def run(self):
        virtualenv_command = self.get_finalized_command('virtualenv')
        virtualenv_command.pip_sync(self.requirement)

    subcommands = [
    ]


class pip_compile(Command):

    description = 'compile a requirements file.'

    user_options = [
        (
            'find-links=', 'f',
            'Look for archives in this directory or on this HTML page'
        ), (
            'no-index', None,
            'Add index URL to generated file',
        ), (
            'upgrade', 'U',
            'Try to upgrade all dependencies to their latest versions',
        ), (
            'output-file=', 'o',
            'output file [default: %s]' % (requirements_path,)
        ), (
            'sources=', 'c',
            'source files [default: %s]' % (install_requires_filename,)
        )
    ]

    def initialize_options(self):
        self.find_links = None
        self.no_index = 0
        self.upgrade = 0
        self.output_file = requirements_path
        self.sources = install_requires_filename

    def finalize_options(self):
        self.ensure_string('output_file')
        self.ensure_string_list('find_links')
        self.ensure_string_list('sources')
        self.find_links = self.find_links or ()
        self.find_links = filter(lambda x: x, self.find_links)
        self.dump_options()

    def run(self):
        virtualenv_command = self.get_finalized_command('virtualenv')
        virtualenv_command.pip_compile(
            self.output_file,
            self.sources,
            find_links=self.find_links,
            no_index=self.no_index,
        )


@setup_dir
def main():
    setuptools = import_setuptools()
    setup_info['cmdclass'] = {
        'build': build,
        'virtualenv': virtualenv,
        'virtualenv_bootstrap_script': virtualenv_bootstrap_script,
        'pip_sync': pip_sync,
        'pip_compile': pip_compile,
    }
    setuptools.setup(**setup_info)


if __name__ == '__main__':
    main()
