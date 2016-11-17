strings2pot
===========

strings2pot is useful to convert Apple .strings, Android/Java .xml or Google app resource bundle .arb files to POT gettext files.


Installation
------------

::

  pip install strings2pot


Command line usage
------------------

::

  root@host$ strings2pot <STRINGS_FILE> <POT_FILE>

e.g.

::

  root@host$ strings2pot Localizable.strings my_ios_app.pot

  root@host$ strings2pot values.xml my_android_app.pot


Code usage
----------

::

  from strings2pot import strings2pot

  executed, error_message = strings2pot.run("Localizable.strings", "my_ios_app.pot")