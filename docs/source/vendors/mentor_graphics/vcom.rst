vcom
~~~~

Vcom has a single warning format:

<warning keyword>: <filename>(linenumber): (<ID>): <message>

where:

+-------------------------------+-------------------------------------------------+
| Item                          |  Regular Expression Match                       |
+===============================+=================================================+
| warning keyword               | ^** Warning                                     |
+-------------------------------+-------------------------------------------------+
| ID                            | vcom-[0-9]+                                     |
+-------------------------------+-------------------------------------------------+
| filename                      | \\W+                                            |
+-------------------------------+-------------------------------------------------+
| linenumber                    | [0-9]+                                          |
+-------------------------------+-------------------------------------------------+
| message                       | .*$                                             |
+-------------------------------+-------------------------------------------------+


Extracting Warnings
^^^^^^^^^^^^^^^^^^^

The fields filename and message will be combined into a single message.

1.  Search for lines starting with **\** Warning:**
2.  Extract ID
3.  Combine filename and message fields as the message

