Usage
=====

ELFWS can be invoked using **elfws** at the command line prompt:

.. code-block:: bash

   $ elfws
   usage: elfws [-h] {suppress, version}

   Suppresses warnings in EDA logfiles.  Reference documentation is
   located at: http://eda-log-file-warning-suppressor.readthedocs.io/en/latest/index.html

   positional arguments:
     {suppress, version}
       suppress                  Suppress warnings in a logfile
       version                   Displays HCM version information

   optional arguments:
     -h, --help                  show this help message and exit


ELFWS has two subcommands:  suppress and version.

suppress
--------

Use the suppress subcommand to suppress warnings in a logfile.

.. code-block:: bash

   $ elfws suppress {vendor} {tool} {logfile} {suppression_file} [options]

The suppress subcommand includes two other subcommands:  vendor and tool.
The additional subcommands allow for customizing LWS to the particulars of specific logfiles.
Help can be requested at each subcommand to view which options are available.

This format allows for the greatest fexibility in addressing differences between logfiles from different vendors.
It also allows for differences between tools from the same vendor.

+-------------------------------+-------------------------------------------------+
| Option                        |  Description                                    |
+===============================+=================================================+
| vendor                        | Which vendor the logfile belongs to.            |
+-------------------------------+-------------------------------------------------+
| tool                          | Which tool the logfile belongs to.              |
+-------------------------------+-------------------------------------------------+
| logfile                       | The logfile to analyze for warnings.            |
+-------------------------------+-------------------------------------------------+
| suppression_file              | The suppression file which has the suppression  |
|                               | rules.                                          |
+-------------------------------+-------------------------------------------------+
| --report                      | Filename of audit report to generate.           |
+-------------------------------+-------------------------------------------------+
| --junit                       | Filename of JUnit XML file to generate.         |
+-------------------------------+-------------------------------------------------+

.. code-block:: bash

   <jcl - need something here after it is coded.>

version
-------

Use the version subcommand to report the installed version of ELFWS.

.. code-block:: bash

   $ elfws version

   <jcl - add something here when it is coded>

