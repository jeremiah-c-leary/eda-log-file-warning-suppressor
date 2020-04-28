Precision
~~~~~~~~~

Precision has two warning formats:  those with IDs and those without.

Warnings With IDs
^^^^^^^^^^^^^^^^^

Warnings with IDs are identified with the Warning keyword and the ID between colons inside square brackets.

<warning keyword>:[<ID>]: "<filename>", <linenumber>: <module>: <message>

where:

+-------------------------------+-------------------------------------------------+
| Item                          |  Regular Expression Match                       |
+===============================+=================================================+
| warning keyword               | ^# Warning                                      |
+-------------------------------+-------------------------------------------------+
| ID                            | [0-9]+                                          |
+-------------------------------+-------------------------------------------------+
| filename                      | \\W+                                            |
+-------------------------------+-------------------------------------------------+
| linenumber                    | line\\s[0-9]+                                   |
+-------------------------------+-------------------------------------------------+
| module                        | Module\\s\\W+                                   |
+-------------------------------+-------------------------------------------------+
| message                       | .*$                                             |
+-------------------------------+-------------------------------------------------+

Warnings Without IDs
^^^^^^^^^^^^^^^^^^^^

Warnings without IDs are identified with the Warning keyword without the ID in square brackets.
The message is considered to be everything after the first colon.

<warning keyword> : <message1> : <message2>

where:

+-------------------------------+-------------------------------------------------+
| Item                          |  Regular Expression Match                       |
+===============================+=================================================+
| warning keyword               | ^Warning                                        |
+-------------------------------+-------------------------------------------------+
| message1                      | .*                                              |
+-------------------------------+-------------------------------------------------+
| message2                      | .*$                                             |
+-------------------------------+-------------------------------------------------+

Extracting Warnings
^^^^^^^^^^^^^^^^^^^

The fields filename, linenumber, module and message will be combined into a single message.

1.  Search for lines starting with **# Warning:**
2.  Extract string from between colons
3.  Classify warning

    a. As ID if there are no spaces within the extracted string
    b. As NO_ID if the there are spaces within the extracted string

4.  Save the message

    a.  Everything after the second colon if the message has an ID
    b.  Everything after the first colon if the message does not have an ID

