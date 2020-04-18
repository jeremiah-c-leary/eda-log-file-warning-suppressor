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

