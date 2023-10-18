Synplify Pro
~~~~~~~~~~~~

Synplify Pro provides warnings on a single line with the line starting with :code:`@W`.

<warning keyword> : <ID> : <message>

where:

+-------------------------------+-------------------------------------------------+
| Item                          |  Regular Expression Match                       |
+===============================+=================================================+
| warning keyword               | @W                                              |
+-------------------------------+-------------------------------------------------+
| ID                            | \\W+                                            |
+-------------------------------+-------------------------------------------------+
| message                       | .*$                                             |
+-------------------------------+-------------------------------------------------+

Extracting Warnings
^^^^^^^^^^^^^^^^^^^

Extraction of warnings from the logfile will follow this process:

1.  Search for lines starting with **@W**
2.  Extract warning keyword
3.  Extract message

