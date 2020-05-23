Vivado
~~~~~~

Vivado has a single warning format, but two different type of warnings:  critical warnings and non critical warnings.
Some warning messages can also span multiple lines.

Critical Warnings
^^^^^^^^^^^^^^^^^

Warnings with IDs are identified with the Warning keyword and the ID between colons.
The message is after the second colon.

<warning keyword>: [<ID>] <message>

where:

+-------------------------------+-------------------------------------------------+
| Item                          |  Regular Expression Match                       |
+===============================+=================================================+
| warning keyword               | ^CRITICAL WARNING                               |
+-------------------------------+-------------------------------------------------+
| ID                            | \\W+\s\W+                                       |
+-------------------------------+-------------------------------------------------+
| message                       | .*$                                             |
+-------------------------------+-------------------------------------------------+

Non Critical Warnings
^^^^^^^^^^^^^^^^^^^^^

Non critical warnings are identical to critical warnings except the keyword.

<warning keyword>: [<ID>] <message>

where:

+-------------------------------+-------------------------------------------------+
| Item                          |  Regular Expression Match                       |
+===============================+=================================================+
| warning keyword               | ^WARNING                                        |
+-------------------------------+-------------------------------------------------+
| ID                            | \\W+\s\W+                                       |
+-------------------------------+-------------------------------------------------+
| message                       | .*$                                             |
+-------------------------------+-------------------------------------------------+

Multiline Warnings
^^^^^^^^^^^^^^^^^^

Multiline warnings can span any number of lines.
They are identified with at least on space at the beginning of the line for each line after the initial warning line.

<warning keyword>: [<ID>] <message1>
<warning continuation><message2>
<warning continuation><message3>

where:

+-------------------------------+-------------------------------------------------+
| Item                          |  Regular Expression Match                       |
+===============================+=================================================+
| warning keyword               | ^[WARNING|CRITICAL WARNING]                     |
+-------------------------------+-------------------------------------------------+
| ID                            | \\W+\s\W+                                       |
+-------------------------------+-------------------------------------------------+
| message1                      | .*$                                             |
+-------------------------------+-------------------------------------------------+
| warning continuation          | ^\s+                                            |
+-------------------------------+-------------------------------------------------+
| message2                      | .*$                                             |
+-------------------------------+-------------------------------------------------+
| message3                      | .*$                                             |
+-------------------------------+-------------------------------------------------+

Extracting Warnings
^^^^^^^^^^^^^^^^^^^

Extraction of warnings from the logfile will follow this process:

1.  Search for lines starting with **WARNING** or **CRITICAL WARNING**
2.  Extract ID and message
3.  Check successive lines for line beginning with spaces

  a.  append line to existing message

