Overview
--------

EDA Log File Warning Suppressor (ELFWS) provides warning suppression for EDA log files.

Why ELFWS?
##########

ELFWS was created after trying to triage warnings in the Mentor Graphics Precision and Microsemi Designer tools.
Precision had a built in method to suppress warnings, but only at the warning ID level.
There was not enough granularity to allow suppression of individual warnings.
Designer does not provide the ability to suppress warnings in their log file.

I like to run through the synthesis and place and route tools early in the design to discover any issues with IP.
This worked well the first time I went through the design as I found an issue with two PLLs.
The issue was fixed and design continued.
When the design was almost completed, I triaged the warnings again and found something new.
This required another change to one of the PLLs.

The new warning was buried with warnings I had previously reviewed.
It was difficult to detect by scanning the file.
It wasn't until I started grepping out those warnings I had seen before that I discovered the new one.
If I was able to properly suppress the warnings I had reviewed before, the new issue would have easily been detected.

I also use Continuous Integration (CI) tools when designing to ensure design quality.
Having to manually triage the warnings each time precludes the use of CI.
If ELFWS had existed, the second issue with the PLL would have been detected much earlier in the design phase.

Key Benefits
############

* Provides a common method to suppress warnings
* Suppress warnings on supported EDA vendor tools
* Additional vendor tools can be added
* Reduce warning triage time

Key Features
############

* Command line tool
* Continuous Integration support

  * JUnit XML output of unsuppressed warnings

* Define suppression rules using YAML
* Reports for auditing suppressed warnings

  * Warnings not suppressed
  * Which warnings were suppressed by which suppression rule
  * Suppression rules which did not suppress any warnings
  * Warnings suppressed by multiple rules

* Operates on the log file

  * Do not need to re-run tool to validate warnings are suppressed
