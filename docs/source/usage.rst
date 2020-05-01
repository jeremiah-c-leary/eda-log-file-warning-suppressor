Usage
=====

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

