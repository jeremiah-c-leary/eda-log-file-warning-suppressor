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

ELFWS can be invoked using **elfws** at the command line prompt:

.. code-block:: bash

   $ elfws
   usage: elfws [-h] {create,report,show,suppress,version} ...
   
   Suppresses Warnings in logfiles.
   
   positional arguments:
     {create,report,show,suppress,version}
       create              Create suppression file
       report              Generate an audit report
       show                Show warnings in logfiles
       suppress            Suppresses warnings in logfiles
       version             Displays ELFWS version information
   
   optional arguments:
     -h, --help            show this help message and exit

ELFWS has five subcommands:  create, report, show, suppress and version.

create
------

Use the create subcommand to generate a suppression rule file from a given warning file.

This can be used as a starting point for a suppression file.
Care should be taken as the output messages are not formatted to support regular expressions.

The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

   $ elfws create -h
   usage: elfws create [-h] [--suppression_file SUPPRESSION_FILE]
                       log_file output_suppression_file

   positional arguments:
     log_file              Log file with warnings to extract
     output_suppression_file
                           Suppression file to create

   optional arguments:
     -h, --help            show this help message and exit
     --suppression_file SUPPRESSION_FILE
                           Existing suppression file to filter out existing

report
------

Use the report subcommand to generate detailed output of suppression warnings.

The report will show the following information:

* Unsuppressed warnings
* Which suppression rules suppressed which warnings
* Unused suppression rules
* Warnings that were suppressed by multiple suppression rules
* Summary of suppression rules and warnings

The report can be used during reviews to ensure the suppressions are valid.

This command has the option argument **--junit**, which will output a JUnit XML file.
This file can be used with continuous integration tools to check for new warnings.

The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

   $ elfws report -h
   usage: elfws report [-h] [--junit JUNIT] log_file suppression_file report_file
   
   positional arguments:
     log_file          Log file to check for warnings
     suppression_file  YAML formatted warning suppression file
     report_file       Output report file
   
   optional arguments:
     -h, --help        show this help message and exit
     --junit JUNIT     Generate JUnit XML file JUNIT

show
----

Use the show subcommand to list all the warnings in a logfile.

This can be useful when first starting out suppressing warnings and a suppression rule file does not exist.

The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

   $ elfws show -h

   usage: elfws show [-h] log_file

   positional arguments:
     log_file    Log file to show warnings

   optional arguments:
     -h, --help  show this help message and exit

suppress
--------

Use the suppress subcommand to suppress warnings in a logfile.

This can be useful when creating a suppression rule file.
It reports the results to the screen and only shows warnings which have not been suppressed.

This subcommand can also be used to support a continuous integration (CI) flow using the *--junit* option.
The *--junit* option will create a JUnit XML file which can be read by CI tools.

The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

   $ elfws suppress -h

   usage: elfws suppress [-h] log_file suppression_file

   positional arguments:
     log_file          Log file to check for warnings
     suppression_file  YAML formatted warning suppression file

   optional arguments:
     -h, --help        show this help message and exit

version
-------

Use the version subcommand to report the installed version of ELFWS.

There are no arguments for this subcommand.

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
