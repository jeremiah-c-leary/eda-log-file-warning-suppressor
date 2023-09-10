Quasta CDC
##########

Questa CDC provides several reports which can be parsed.

cdc_run.log
===========

The cdc_run.log file reports violations, cautions, and evaluations in addition to run time errors and warnings.

CDC Results
^^^^^^^^^^^

This section reports the CDC crossings and whether they are Violations, Cautions, and Evaluations.
The reporting is divided into reporting the number of types of crossings and then the details of the crossing.
Only the number of types of crossings will be reported for Violations, Cautions, and Evaluations.

Message Summary
^^^^^^^^^^^^^^^

This section reports errors and warnings encountered while running the tool.
There should not be any Errors or Warnings in this section.

cdc_detail.rpt
==============

The cdc_detail.rpt file provides the most items to be checked.

Section 1 : Clock Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The number of inferred clocks should be 0.
The following line will be checked:

2. Inferred     :(0)

If the number in the parenthesis is not 0, then a warning will be reported.

Section 2 : Reset Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The number of inferred resets should be 0.
The following line will be checked:

2. Inferred     :(0)

If the number in the parenthesis is not 0, then a warning will be reported.

Section 3 : CDC Results
^^^^^^^^^^^^^^^^^^^^^^^

This section reports the CDC crossings and whether they are Violations, Cautions, and Evaluations.
The reporting is divided into reporting the number of types of crossings and then the details of the crossing.
Only the number of types of crossings will be reported for Violations, Cautions, and Evaluations.

Section 9 : Design Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section reports information about the design.
The number of empty modules and unresolved modules should be 0 to ensure a proper analysis.

The following lines will be checked:

Number of Empty Modules  = 0
Number of Unresolved Modules = 0

If the number after the equal sign is not 0, then a warning will be reported.

Section 10 : Port Domain Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section reports each port and the clock assigned to it.
It also reports whether the user defined the clock domain or if QuestaCDC assigned it.

Each line follows this format:

<Port> <Direction> <Constraints> {<Clock Domain>} <Type>

If <Type> is not "User" then an warning will be reported.

