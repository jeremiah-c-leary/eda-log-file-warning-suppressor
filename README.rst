EDA Log File Warning Suppressor (ELFWS)
=======================================

**Suppresses warnings in EDA logfiles.**

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

ELFWS was created after going through a warning validation for an FPGA design.
The synthesis tool provided the ability to suppress warnings, but only at the warning id level.
The place and route tool did not supply any ability to suppress warnings.
This eventually led to a situation where a warning was induced by a design change.
Unfortunately, it was not detected until much later in the design phase.
A design change was required to remove the warning, and fortunately the change was minor.
It could have turned out much worse.

Key Benefits
------------

* Provides standard for defining warning suppressions
* Provides warning suppression for tools that do not support suppressions

Key Features
------------

* Warning definition

  * Uses YAML to define suppression rules
  * Can include justifications for warning suppression

* Continuous Integration tools

  * command line tool
  * outputs JUnit XML files

* Reports

  * lists which rules suppressed which warnings
  * lists rules which did not suppress any warnings
  * lists warnings which were suppressed by multiple rules

