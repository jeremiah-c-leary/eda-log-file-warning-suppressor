Suppression Rules
=================

The suppression rules are a YAML formatted file with the following basic form:

.. code-block:: yaml

   suppress:
     no_id:
       msg: 'Unused port'
       comment: 'This port is not used.'
       author: 'mpw'
     <warning_id>:
       msg: 'Port I_CLK not used'
       comment: 'This port is not used.'
       author: 'jcl'

.. jcl - I need to mess with the formatting some more to get what I really want.

it starts with the **suppress** element.
This is further divided into one or more elements:

+--------------------+----------+-------------------------------------------------+
| Suppress Option    | Required |  Description                                    |
+====================+==========+=================================================+
| no_id              |          | Not all warning messages have identifiers.      |
|                    |   No     | Those warnings without identifiers which are    |
|                    |          | to be suppressed are documented here.           |
+--------------------+----------+-------------------------------------------------+
| <warning_id>       |   No     | This is the unique identifier for a warning.    |
|                    |          | The only restriction is there can be no spaces. |
+--------------------+----------+-------------------------------------------------+

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

.. jcl - Need some real world examples that show the warning message and a corresponding suppression rule.
