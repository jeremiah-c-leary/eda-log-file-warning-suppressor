Theory of Operation
===================

ELFWS performs the following tasks:

1. Read suppression rule file
2. Read logfile
3. Determine vendor
4. Load warning extractor
5. Extract warnings from logfile
6. Compare suppression rules against extracted warnings
   a.  Mark which rule suppressed a warning
7. Report results

Read suppression rule file
--------------------------

This reads the YAML file which will create a dictionary.

Read logfile
------------

This reads the text logfile and stores it as a list of strings.

Determine vendor
----------------

The log file will be interrogated to determine the vendor log file.

Load warning extractor
----------------------

There are different patterns of warnings depending on the vendor and tool.
To support multiple styles, each vendor and tool will require it's own warning extractor.

Extract warnings from logfile
-----------------------------

The logfile is parsed using the loaded warning extractor.
Any warning discovered will be stored in a list for further analysis.

Compare suppression rules against extracted warnings
----------------------------------------------------

Each warning will be compared against every suppression rule.
If a match is found then that warning will be stored with the rule.
If not match is found then that warning will be stored in an unmatched list.

Report results
--------------

The format of the reporting results will depend on the subcommand chosen.
Refer to the subcommand for further details.
