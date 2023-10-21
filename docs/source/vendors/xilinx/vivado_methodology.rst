Vivado Methodology
~~~~~~~~~~~~~~~~~~

The Vivado methologoy report has a single warning format, but two different type of warnings:  critical warnings and non critical warnings.
Some warning messages can also span multiple lines.

Methodology Format
^^^^^^^^^^^^^^^^^^

Each methodology violation is reported over multiple lines.

<ID>#<count> <classification>
<description>
<details>
Related violations: <related>

where:

+-------------------------------+-------------------------------------------------+
| Item                          |  Regular Expression Match                       |
+===============================+=================================================+
| ID                            | \W+                                             |
+-------------------------------+-------------------------------------------------+
| count                         | [0-9]+                                          |
+-------------------------------+-------------------------------------------------+
| classification                | \W+                                             |
+-------------------------------+-------------------------------------------------+
| details                       | \\W+\s\W+                                       |
+-------------------------------+-------------------------------------------------+
| related                       | \\W+\s\W+                                       |
+-------------------------------+-------------------------------------------------+

Extracting Warnings
^^^^^^^^^^^^^^^^^^^

Extraction of warnings from the logfile will follow this process:

1.  Search for second line starting with 2. REPORT DETAILS
2.  Extract ID and drop count and classification
3.  drop description
4.  Extract details
5.  drop related

