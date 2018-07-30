coala-pyflakes
-----------

coala-pyflakes offers bears and plugins built on top of
`pyflakes enhanced AST <https://github.com/PyCQA/pyflakes>`__. Bears are
desiged to work with `coala infrastructure <https://github.com/coala/coala>`__
whereas generic plugins can be integrated with `flake8 <https://github.com/PyCQA/flake8/>`__ wrapper.

============
Installation
============

To install the **latest stable version**, run:

.. code-block:: bash

    $ pip3 install coala-pyflakes

|Stable|

To install the latest development version, run:

.. code-block:: bash

    $ pip3 install coala-pyflakes --pre

Be sure to use the latest version of pip, the default pip from Debian doesn't
support our dependency version number specifiers. You will have to `use a
virtualenv <https://github.com/coala/coala/wiki/FAQ#installation-is-failing-help>`__
in this case.

To install generic plugins follow the flake8
`guide <http://flake8.pycqa.org/en/latest/plugin-development/registering-plugins.html>`__
to register a plugin.

|Linux|

-----

=====
Usage
=====

For more information about how to do basic analysis, check out the
`coala README <https://github.com/coala/coala#usage>`__.

-----

================
Getting Involved
================

If you would like to be a part of the coala community, you can check out our
`Getting In Touch <http://coala.readthedocs.io/en/latest/Help/Getting_In_Touch.html>`__
page or ask us at our active Gitter channel, where we have maintainers from
all over the world. We appreciate any help!

We also have a
`newcomer guide <http://coala.io/newcomer>`__
to help you get started by fixing an issue yourself! If you get stuck anywhere
or need some help, feel free to contact us on Gitter or drop a mail at our
`newcomer mailing list <https://groups.google.com/d/forum/coala-newcomers>`__.

|gitter|

-----

=======
Support
=======

Feel free to contact us at our `Gitter channel <https://gitter.im/coala/coala>`__, we'd be happy to help!

For any issues regarding AST contact us on our `ast room <https://gitter.im/coala/ast>`__.

If you are interested in commercial support, please contact us on the Gitter
channel as well.

You can also drop an email at our
`mailing list <https://github.com/coala/coala/wiki/Mailing-Lists>`__.

-----

=======
Authors
=======

coala-pyflakes is maintained by a growing community. Please take a look at the
meta information in `setup.py <https://gitlab.com/MacBox7/coala-pyflakes/blob/master/setup.py>`__ for the current maintainers.

-----

=======
License
=======

|MIT|


.. |Stable| image:: https://img.shields.io/badge/latest%20stable-0.1-green.svg
.. |Linux| image:: https://gitlab.com/MacBox7/coala-pyflakes/badges/master/build.svg
.. |gitter| image:: https://img.shields.io/badge/gitter-join%20chat%20%E2%86%92-brightgreen.svg
   :target: https://gitter.im/coala/coala
.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT)
