mete0r.testfixture
==================

a testfixture helper


Quickstart
----------

To install::

   pip install mete0r.testfixture


Let's assume your project has following structure::

   yourproject/
       setup.py
       yourpackage/
           __init__.py
           tests/
               __init__.py
               test_foo.py
               fixtures/
                   foo.py
                   bar.py


Define a fixture in ``yourpackage/tests/fixtures/foo.py``::

   from mete0r_testfixture.testfixture import testfixture

   @testfixture('Foo')
   def foo(fixtures):
       return {
           'foo': None,
       }

Define another fixture in ``yourpackage/tests/fixtures/bar.py``::

    @testfixture('Bar', 'foo')
    def bar(fixtures):
        return {
            'bar': fixtures.get('Foo')
        }

Now you can use them in your tests::

    # yourpackage/tests/test_foo.py
    from unittest import TestCase
    from mete0r_testfixture.testfixture import TestFixtures
    from . import fixtures

    class FooTest(TestCase):

        def test_foo(self):
            testfixtures = TestFixtures(fixtures)
            self.assertEquals({
                'bar': {
                    'foo': None,
                },
            }, testfixtures.get('Bar', 'foo')


You can also list test fixtures defined in your packages::

   $ mete0r-testfixture-scan yourpackage
   Foo	        yourpackage.tests.fixtures.foo.foo
   Bar, foo	yourpackage.tests.fixtures.bar.bar


Development environment
-----------------------

To setup development environment::

   python setup.py virtualenv
   make
