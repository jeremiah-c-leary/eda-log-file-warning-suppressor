Overview
--------

Logfile Warning Suppressor (LWS) provides warning suppression for EDA log files.

Why LWS?
########

.. jcl - Apr 10, 2020: need to review this section

LWS was created after trying to vett warnings in the Mentor Graphics Precision and Microsemi Designer tools.
Precision had a built in method to suppress warnings, but only at the warning number level.
There was not enough granularity to allow suppression of individual warnings.
Designer does not have the capability to suppress warnings in their log file.

I like to run through the synthesis and place and route tools early in the design to discover any issues with IP.
This worked well the first time I went through the design as I found an issue with two PLLs.
The issue was fixed and design continued.
When the design was almost completed, I vetted the warnings again and found something new.
This required another change to one of the PLLs.

The new warning was buried in with warnings I had previously reviewed.
It was difficult to detect by scanning the file.
Most of the warnings I had seen before and I became complacent.
It wasn't until I started grepping out those warnings I had seen before that I discovered the new one.

I also use Continuous Integration (CI) tools when designing to ensure design quality.
Having to manually vett the warnings each time precludes the use of CI.
If LWS had existed, the second issue would have been detected much earlier in the design phase.

Key Benefits
############

* Common method to suppress warnings across multiple EDA vendor tools
* Allows CI tool integration
* Warning suppressions can be configuration managed

Key Features
############

* Command line tool
* Integrates into CI flow tools using JUNIT.XML files
* Uses YAML to define suppressed warnings
* Reports for auditing suppressions
  * Warnings not suppressed
  * Which warnings were suppressed by which suppression rule
  * Suppression rules which did not suppress any warnings
  * Warnings suppressed by multiple rules
