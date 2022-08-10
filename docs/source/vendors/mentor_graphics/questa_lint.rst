Quasta Lint
~~~~~~~~~~~~

Questa Lint has a single format for errors, warnings and infos.

<ID>: <message>, Module '<module>', File '<filename>', Line '<linenumber>' 

where:

+-------------------------------+-------------------------------------------------+
| Item                          |  Regular Expression Match                       |
+===============================+=================================================+
| ID                            | \\W+                                            |
+-------------------------------+-------------------------------------------------+
| filename                      | \\W+                                            |
+-------------------------------+-------------------------------------------------+
| linenumber                    | \\s[0-9]+                                       |
+-------------------------------+-------------------------------------------------+
| module                        | \\W+                                            |
+-------------------------------+-------------------------------------------------+
| message                       | .*$                                             |
+-------------------------------+-------------------------------------------------+

Extracting Warnings
^^^^^^^^^^^^^^^^^^^

The fields filename, linenumber, module and message will be combined into a single message.

1.  Search for line starting with 'Section 2' before processing warnings
2.  Search for lines starting with 'Check:'

    a.  extract ID

3.  Search for lines starting with extracted ID

    a.  create warning

4.  Search for a line starting with '| Info'

    a.  Stop searching for 
