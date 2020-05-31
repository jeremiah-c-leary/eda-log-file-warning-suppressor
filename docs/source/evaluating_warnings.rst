Evaluating Warnings
===================

The process for evaluating warnings looks like this:

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

The initials of the person doing the classification should be given in the **author** field of the suppression rule.
This indicates to other users who to contact about the suppression if there are any questions.

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
* warnings you need to input from someone else

Each warning, or groups of warnings, which need investigation should be tracked.
This can be done with a spreadsheet or a dedicated issue tracking system.

Depending on the result of the investigation, the warning will either be suppressed or mitigated.

In ELFWS these types of warnings will be suppressed, but will be tagged with an **investigate** field in the suppression rule.
The **investigate** field can be used as a pointer to into a tool used to track issues.

Use the **comment** field to document questions about the warning to be investigated.

If the warning is eventually mitigated, then the suppression will be removed from the suppression file.
if the warning is eventually suppressed, then remove the **investigate** field and update the comment to indicate why the warning can be suppressed.

