User Tool Files
---------------

ELFWS allows the user to define their own local tool files.
This is accomplished by creating a local vendor directory and setting an environment variable.

Creating a User Vendor Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the following directory structure for vendors and their tools:

.. code-block:: text

    <user_vendor_directory>
     |
     +-- <vendor name>
          |
          +-- <tool_name>.py

Refer to Adding Vendor Tools for more information on this directory structure.

Setting the Environment Variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set the environment variable :code:`ELFWS_USER_VENDOR_DIR` to the location of the user vendor directory.
ELFWS will search for a matching tool file in the user vendor directory before searching for an ELFWS tool file.

Parser Search Order
~~~~~~~~~~~~~~~~~~~

Vendor directories and tool files are searched in alphabetical order.
The first tool file whose :code:`is_logfile` function returns True is used.
Only files ending in :code:`.py` are loaded, and :code:`__init__.py` and :code:`utils.py` are ignored.
If a tool file cannot be imported, ELFWS prints a warning with the file path and continues searching.
