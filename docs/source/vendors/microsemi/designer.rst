Designer
~~~~~~~~

Designer has two different warning formats:  those with ID's and those without.
Warning messages can also span multiple lines.

Warnings With IDs
^^^^^^^^^^^^^^^^^

Warnings with IDs are identified with the Warning keyword and the ID between colons.
The message is after the second colon.

<warning keyword> : <ID> : <message>

where:

+-------------------------------+-------------------------------------------------+
| Item                          |  Regular Expression Match                       |
+===============================+=================================================+
| warning keyword               | ^Warning                                        |
+-------------------------------+-------------------------------------------------+
| ID                            | \\W+                                            |
+-------------------------------+-------------------------------------------------+
| message                       | .*$                                             |
+-------------------------------+-------------------------------------------------+

Warnings Without IDs
^^^^^^^^^^^^^^^^^^^^

Warnings without IDs are identified with the Warning keyword and colon.
The message is after the colon.

<warning keyword> : <message>

where:

+-------------------------------+-------------------------------------------------+
| Item                          |  Regular Expression Match                       |
+===============================+=================================================+
| warning keyword               | ^Warning                                        |
+-------------------------------+-------------------------------------------------+
| message                       | .*$                                             |
+-------------------------------+-------------------------------------------------+

Multiline Warnings
^^^^^^^^^^^^^^^^^^

Multiline warnings can span any number of lines.
They are identified with at least on space at the beginning of the line for each line after the initial warning line.

<warning keyword> : <ID> : <message1>
<warning continuation><message2>
<warning continuation><message3>

where:

+-------------------------------+-------------------------------------------------+
| Item                          |  Regular Expression Match                       |
+===============================+=================================================+
| warning keyword               | ^Warning                                        |
+-------------------------------+-------------------------------------------------+
| ID                            | \\W+                                            |
+-------------------------------+-------------------------------------------------+
| message1                      | .*$                                             |
+-------------------------------+-------------------------------------------------+
| warning continuation          | ^\s+                                            |
+-------------------------------+-------------------------------------------------+
| message2                      | .*$                                             |
+-------------------------------+-------------------------------------------------+
| message3                      | .*$                                             |
+-------------------------------+-------------------------------------------------+

..or

<warning keyword> : <message1>
<warning continuation><message2>
<warning continuation><message3>

where:

+-------------------------------+-------------------------------------------------+
| Item                          |  Regular Expression Match                       |
+===============================+=================================================+
| warning keyword               | ^Warning                                        |
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

1.  Search for lines starting with **Warning**
2.  Classify warning

  a.    As ID if ID pattern matches
  b.    As no_id if ID pattern does not match

3.  Check successive lines for line beginning with spaces

  a.  append line to existing message
