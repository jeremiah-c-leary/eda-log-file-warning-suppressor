Theory of Operation
===================

LWS performs the following tasks in this order:

1. Read suppression rule file
2. Read logfile
3. Extract warnings from logfile
4. Compare suppression rules against extracted warnings
   a.  Mark which rule suppressed a warning
5. Report results
   a.  Send unsuppressed warnings to stdio
   b.  Generate JUnitXML file if requested
   c.  Generate audit report if requested

Read suppression rule file
--------------------------

This just reads the YAML file which will create a dictionary.

Read logfile
------------

This reads the text logfile and stores it as a list of strings.

Extract warnings from logfile
-----------------------------

There are different patterns of warnings depending on the vendor and tool.
To support multiple styles, each vendor and tool will require it's own extractor.

.. jcl - detail how we handle multiple vendors and their tools

Compare suppression rules against extracted warnings
----------------------------------------------------

Each warning will be compared against every suppression rule.
If a match is found then that warning will be stored with the rule.
If not match is found then that warning will be stored in an unmatched list.

Report results
--------------

All unmatched rules will be sent to stdio for the user to see.
If the user requested a JUnitXML file to support CI, it will be generated at this step.
If the user requested an audit report, it will be generated at this step.

