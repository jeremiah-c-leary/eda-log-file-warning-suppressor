Evaluating Warnings
===================

There is a natural process for evaluating warnings.
The process follows the diagram below:

.. code-block:: text

   warning -> evaluate -+-> suppress
                        |
                        +-> mitigate
                        |
                        +-> investigate -+-> suppress
                                         |
                                         +-> mitigate

Evaluate
--------

During the evaluate phase, the warning is reviewed.
One of three classifications will be applied:  suppress, mitigate or investigate.

Suppress
--------

If the warning can be safely ignored, then it can be suppressed.

A justification for suppressing should be given in the **comment** field of the suppression rule.
Giving the justification documents the reasoning behind suppressing.
This communicates the intent for other users and as a reminder to the author why the warning was suppressed.

The name, or initials, of the person doing the classification should be given in the **author** field of the suppression rule.
This indicates to other users who to contact if there are questions about the suppression rule.

Mitigate
--------

The warning could point to a real issue in the design.
Addressing the issue will lead to the warning no longer being reported by the tool.

Investigate
-----------

If the warning requires a significant amount of time to evaluate, it falls into the investigate classification.
This can happen for any of the following reasons:

* warnings in vendor IP
* warnings in a part of code base you are unfamiliar with
* warnings requiring someone else to evaluate

Each warning which requires investigation should be tracked.
This can be done with a spreadsheet or a dedicated issue tracking system.

Depending on the result of the investigation, the warning will either be suppressed or must be mitigated.

In ELFWS these types of warnings will be suppressed, but can be tagged with an **investigate** field in the suppression rule.

Use the **comment** field to document questions about the warning to be investigated.
The tracking ID can be added to the **comment** field.

If the warning under investigation is mitigated, then the suppression rule should be removed from the suppression file.
If the warning under investigation is suppressed, then remove the **investigate** field and update the comment to indicate why the warning can be suppressed.

