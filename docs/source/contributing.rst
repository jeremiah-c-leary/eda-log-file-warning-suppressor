Contributing
------------

I welcome any contributions to this project.

There are several ways to contribute:

1. Bug reports
2. Code base improvements
3. Feature requests
4. New vendor warning suppressions

Bug Reports
###########

If you run into anything that is not handled correctly, please submit an issue.
When creating the issue, use the **bug** label to highlight it.
Fixing bugs is prioritized over feature enhancements.

Code Base Improvements
######################

My Python journey is never ending and I learn new things with each project.
I run the code through *Codacy* and *Code Climate*, and they are very helpful.
However, I would appreciate any suggestions to improve the code base.

Create an issue and use the **refactor** label for any code which could be improved.

Code Checks
###########

Every pull request runs these checks, in addition to the unit tests.
Run them locally before submitting (they require Python 3.11 or newer):

.. code-block:: bash

   pip install pyflakes sdsort

   python -m unittest
   pyflakes elfws $(find tests -name '*.py' -not -path 'tests/user_defined_tools/*')
   sdsort --check elfws

* **pyflakes** reports unused imports and variables, and undefined names.
* **sdsort** checks that functions follow the *Stepdown Rule*: each function is defined below the functions which use it, so the code reads from top to bottom.
  Running :code:`sdsort elfws` without :code:`--check` reorders the functions for you.

Feature Requests
################

Let me know if there is anything I could add to make ELFWS easier to use.
Create an issue with the **enhancement** label.

New Vendor Warning Suppresssions
################################

I plan to update ELFWS as I run into tools where I need to suppress warnings.
If there is a tool that is currently not supported, then create an issue with the **Vendor Tool** label.

Provide a small sample showing the format of the warnings and I can add it or show you how to add it.

Releasing
#########

Publishing a GitHub release uploads ELFWS to PyPI automatically.

1. Update the version in :code:`elfws/version.py` and the release notes, and merge them to master.
2. Create a GitHub release whose tag is the version number, without a leading *v* (for example :code:`0.12.0`).

The release fails without publishing anything if the tag does not match :code:`elfws/version.py`.
