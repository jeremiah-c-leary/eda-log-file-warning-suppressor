Precision
~~~~~~~~~

Precision has a single warning format:

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


Extracting Warnings
^^^^^^^^^^^^^^^^^^^

The fields filename, linenumber, module and message will be combined into a single message.

1.  Search for lines starting with **# Warning:**
2.  Extract ID from between colons
3.  Save everything after the colon after the ID field as the message

