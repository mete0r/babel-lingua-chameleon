babel-lingua-chameleon
======================

Babel extractor for Chameleon templates

Just provides `lingua`_'s `Chameleon`_ message extractor functionality through
`Babel`_ interface.

.. _Babel: https://pypi.org/project/Babel/
.. _Chameleon: https://pypi.org/project/Chameleon/
.. _lingua: https://pypi.org/project/lingua/


Usage
-----

The `extraction method`_ name is ``lingua-chameleon``.

.. _extraction method: http://babel.pocoo.org/en/latest/messages.html#extraction-method-mapping-and-configuration

So in your mapping/configuration files::

   [lingua-chameleon: **/templates/**.pt]

And/or in your setup.py::

    'message_extractors': {
        'MYPACKAGE': [
            ('**.pt', 'lingua-chameleon', None),
        ]
    },


Development environment
-----------------------

To setup development environment::

   python setup.py virtualenv
   make
