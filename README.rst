EDA Log File Warning Suppressor (ELFWS)
=======================================

**Suppresses warnings in EDA logfiles.**

.. image:: https://img.shields.io/github/tag/jeremiah-c-leary/eda-log-file-warning-suppressor.svg?style=flat-square
   :target: https://github.com/jeremiah-c-leary/eda-log-file-warning-suppressor
   :alt: Github Release
.. image:: https://img.shields.io/pypi/v/elfws.svg?style=flat-square
   :target: https://pypi.python.org/pypi/elfws
   :alt: PyPI Version
.. image:: https://img.shields.io/travis/jeremiah-c-leary/eda-log-file-warning-suppressor/master.svg?style=flat-square
   :target: https://travis-ci.org/jeremiah-c-leary/eda-log-file-warning-suppressor
   :alt: Build Status
.. image:: https://img.shields.io/codecov/c/github/jeremiah-c-leary/eda-log-file-warning-suppressor/master.svg?style=flat-square
   :target: https://codecov.io/github/jeremiah-c-leary/eda-log-file-warning-suppressor
   :alt: Test Coverage
.. image:: https://img.shields.io/readthedocs/vsg.svg?style=flat-square
   :target: http://eda-log-file-warning-suppressor.readthedocs.io/en/latest/index.html
   :alt: Read The Docs
.. image:: https://api.codacy.com/project/badge/Grade/3ecbff706c6640fcae47b003b74c71dd    :target: https://www.codacy.com/manual/jeremiah-c-leary/eda-log-file-warning-suppressor?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jeremiah-c-leary/eda-log-file-warning-suppressor&amp;utm_campaign=Badge_Grade
   :alt: Codacy
.. image:: https://api.codeclimate.com/v1/badges/6d41bcbece1f25056bdb/maintainability
   :target: https://codeclimate.com/github/jeremiah-c-leary/logfile-warning-suppressor/maintainability
   :alt: Maintainability



Table of Contents
-----------------

*  `Overview`_
*  `Key Benefits`_
*  `Key Features`_
*  `Installation`_
*  `Usage`_
*  `Documentation`_
*  `Contributing`_

Overview
--------

ELFWS was created after going through warning triage for an FPGA design.
The synthesis tool provided the ability to suppress warnings, but only at the warning id level.
The place and route tool did not supply any ability to suppress warnings.
Eventually a design change induced a new warning.
Unfortunately, it was not detected until much later in the design process.
A design change was required to resolve the warning.
The change was minor, but could have resulted in major design changes if it could not have been resolved.

Key Benefits
------------

* Standardizes warning suppression definition
* Provides warning suppression for tools that do not support suppressions

Key Features
------------

* Warning definition

  * Uses YAML to define suppression rules
  * Can include justifications for warning suppression

* Continuous Integration tool support

  * command line tool
  * outputs JUnit XML files

* Audit Reports

  * which rules suppressed which warnings
  * rules which did not suppress any warnings
  * warnings which were suppressed by multiple rules

Installation
------------

You can get the latest released version of ELFWS via **pip**.

.. code-block:: bash

    pip install elfws

The latest development version can be cloned...

.. code-block:: bash

    git clone https://github.com/jeremiah-c-leary/eda-log-file-warning-supressor.git

...and then installed locally...

.. code-block:: bash

    python setup.py install

Usage
-----

ELFWS can be invoked by issuing **elfws** at the comman dline prompt:

.. code-block:: bash

   $ elfws
   usage: elfws [-h] {suppress,version} ...
   
   Suppresses Warnings in logfiles.
   
   positional arguments:
     {suppress,version}
         suppress          Suppresses warnings in logfiles
         version           Displays ELFWS version information
   
   optional arguments:
     -h, --help            show this help message and exit

ELFWS has two subcommands:  suppress and version.

suppress
~~~~~~~~

Use the **suppress** subcommand to suppress warnings from log files.

The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

    $elfws suppress -h
    usage: elfws suppress [-h] log_file suppression_file
    
    positional arguments:
      log_file          Log file to check for warnings
      suppression_file  YAML formatted warning suppression file
    
    optional arguments:
      -h, --help        show this help message and exit

version
~~~~~~~

Use the **version** subcommand to display the installed version.

.. code-block:: bash

    $ elfws version
    EDA Log File Warning Suppressor (ELFWS) version 1.0.0

Documentation
-------------

All documentation for ELFWS is hosted at `read-the-docs <http://eda-log-file-warning-suppressor.readthedocs.io/en/latest/index.html>`_.

Contributing
------------

I welcome any contributions to this project.
No matter how small or large.

There are several ways to contribute:

* Bug reports
* Code base improvements
* Feature requests

Please refer to the documentation hosted at `read-the-docs <http://eda-log-file-warning-suppressor.readthedocs.io/en/latest/index.html>`_ for more details on contributing.
