Suppression Rules
=================

The suppression rules are a YAML formatted file with the following basic form:

.. code-block:: yaml

   suppress:
     rules:
       <warning_id>:
         - msg: Port I_CLK_A not used
           comment: This port is not used in this design.
           author: jcleary
         - msg: Port I_DATA_A not used'
           comment: This port is not used in this design.
           author: jcleary
           investigate : True
       <warning_id>:
         - msg: Signal fifo_enable is tied high
           comment: The FIFO is always enabled in this design to support data throughput.
           author: jcleary


It starts with the **suppress** key and then a **rules** key.
The **rules** key contains one or more suppression rules.
Each **rules** key is further divided into one or more warning ids.

Warning IDs
-----------

Regular expressons are support in warning ids.
This allows for another method of grouping suppressions.
In the example below, every ID that starts with **Synth-** and has **flip-flop** in the message will be suppressed.

.. code-block:: yaml

   suppress:
     rules:
       Synth-.*:
         - msg: flip-flop

Suppression Rule Fields
-----------------------

Each suppression rule will have the following fields available:

+--------------------+----------+-------------------------------------------------+
| Option             | Required |  Description                                    |
+====================+==========+=================================================+
| msg                |          | The message to suppress. This will be a regular |
|                    |   Yes    | a regular expression which will match after the |
|                    |          | defined message ID.  LSW will prepend a .* to   |
|                    |          | this field.                                     |
+--------------------+----------+-------------------------------------------------+
| comment            |   No     | While optional, it is strongly recommened to    |
|                    |          | use this field to document why the warning was  |
|                    |          | suppressed.                                     |   
+--------------------+----------+-------------------------------------------------+
| author             |   No     | Document who created the suppression.           |
+--------------------+----------+-------------------------------------------------+
| investigate        |   No     | Boolean(True/False) indicating the warnings the |
|                    |          | rule suppresses need further analysis.          |
|                    |          | This defaults to False.                         |
+--------------------+----------+-------------------------------------------------+

In addition to the standard warning ID, each tool may have warnings without IDs.
For example, Microsemi designer has warnings without identifiers.
When processing these warnings, ELFWS will use a warning ID of **no_id**.

.. code-block:: yaml

   suppress:
     no_id:
       msg: Unused port
       comment: This port is not used.
       author: mpw
     <warning_id>:
       msg: Port I_CLK not used
       comment: This port is not used.
       author: jcl

If these unique IDs exist, they are listed in the tool section of this documentation.

Grouping Rules
--------------

It can be helpful to group rules based on some criteria.
For example, file names, sections in a log file, design elements or warning types.

.. code-block:: yaml

   suppress:
     <group id>:
       rules:
         <warning_id>:
           - msg: FIFO uses same clock for read and write

Arbitrary levels of groupings are also supported:

.. code-block:: yaml

   suppress:
     <group id>:
       rules:
         <warning_id>:
           - msg: FIFO uses same clock for read and write
     <group id>:
       <group id>:
         rules:
           <warning_id>:
             - msg: RAM address bits [12:3] are unused
       <group id>:
         rules:
           <warning_id>:
             - msg: invalid false path
       rules:
         <warning_id>:
           - msg: UART is blackboxed
     rules:
       <warning_id>:
         - msg:  signal fifo_wr is tied high

Dividing suppression rules into groups helps with maintaining the suppress rules.
ELFWS flattens all the suppression rules into a single list.

