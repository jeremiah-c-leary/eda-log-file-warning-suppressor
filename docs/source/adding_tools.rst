Adding Vendor Tools
-------------------

To add a new vendor tool, you must understand the ELFWS vendor directory structure.

Directory Structure
~~~~~~~~~~~~~~~~~~~

ELFWS uses the following directory structure for vendors and their tools:

.. code-block:: text

   elfws
    |
    +-- vendor
         |
         +-- <vendor name>
              |
              +-- <tool_name>.py

For example, for our example the tools Microsemi Designer and Mentor Graphics Precision are in this directory structure:

.. code-block:: text

   elfws
    |
    +-- vendor
         |
         +-- mentor_graphics
         |    |
         |    +-- precision.py
         |
         +-- microsemi
              |
              +-- designer.py

The vendor directories and tool files expand as they are added:

.. code-block:: text

   elfws
    |
    +-- vendor
         |
         +-- mentor_graphics
         |    |
         |    +-- precision.py
         |    +-- questa_sim.py
         |
         +-- microsemi
         |    |
         |    +-- designer.py
         |
         +-- synopsys
              |
              +-- synplify_pro.py
              +-- design_compiler.py 

ELFWS will search the elfws->vendor directory for all directories.
It will then search each of those directories for tool files.
ELFWS will pass the log file to each tool file and ask if the log file is from that tool.
If the tool file does not recognize the log file, then ELFWS moves to the next tool.
If the tool file does recognize the log file, then ELFWS uses the extract_warnings function to parse out the warnings in the file.
