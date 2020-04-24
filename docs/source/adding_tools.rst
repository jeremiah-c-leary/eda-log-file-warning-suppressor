Adding Vendor Tools
-------------------

To add a new vendor tool, you must understand the ELFWS directory structure.

directory structure
-------------------

ELFWS uses the following directory structure for vendors and their tools:

``elfws -> vendor -> <vendor_name> -> <tool_name>``

For example, for our example the tools Microsemi Designer and Mentor Graphics Precision are in this directory structure:


``elfws -> vendor -> mentor_graphics -> precision.py``
   
``                -> microsemi       -> designer.py``


The directories and tool files expand as they are added:


``elfws -> vendor -> mentor_graphics -> precision.py``
``                                   -> questsa_sim.py``

``                -> microsemi       -> designer.py``

``                -> synopsis        -> synplify_pro.py``
``                                   -> design_compiler.py``


ELFWS will search the elfws->vendor directory for all directories.
It will then search each <vendor_name> directory for the tool files.
ELFWS will pass the log file to each tool file and ask it to acknowledge if it recognizes it.
If the tool file does not recognize it, then ELFWS moves to the next tool.
If the tool file does recognize it, then EFLWS uses the extract_warnings function to parse out the warnings in the file.


