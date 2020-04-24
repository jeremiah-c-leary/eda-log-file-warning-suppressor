Vendor Tool File
================

The Vendor Tool file performs the initial parsing of warnings from the log file.
It must contain the following functions:

* get_vendor()
* get_tool_name()
* is_logfile()
* extract_warnings()

imports
-------

To support the *extract_warnings* function, the following imports must be included:

.. code-block:: python

   from elfws import warning
   from elfws import warning_list

get_vendor
----------

This function just returns a list of strings listing the vendor.
A list was choosen to manage company acquisitions.
The most recent company name should be first in the list.


.. code-block:: python

   def get_vendor():
       return ['Microsemi', 'Actel']

get_tool_name
-------------

This function returns a string with the name of the tool.

.. code-block:: python

   def get_tool_name():
       return 'designer'


is_logfile
----------

This function is responsible for parsing the logfile and determining whether it is a logfile for the tool.
There is typically some unique strings in the beginning of the logfile that identifies which tool generated it.
The function must return a boolean.

.. code-block:: python

   def is_logfile(lFile):
        for iLineNumber, sLine in enumerate(lFile):
            if sLine.startswith('Microsemi Libero Software'):
                return True
            if iLineNumber == 10:
                return False
        return False

extract_warnings
----------------

This function parses the logfile for warnings.
It returns a warning_list object with a collection of warning objects.

The following code looks for lines starting with *Warning* and then proceeds to handle warnings without IDs and multiline warnings.

.. code-block:: python

   def extract_warnings(lFile):
       oReturn = warning_list.create()
   
       fWarningFound = False
       for iLineNumber, sLine in enumerate(lFile):
           # Clear the warning found flag
           if not sLine.startswith(' ') and fWarningFound:
               fWarningFound = False
               oReturn.add_warning(oWarning)
           if sLine.startswith(' ') and fWarningFound:
               oWarning.message += ' ' + sLine.strip()
           if sLine.startswith('Warning:'):
               fWarningFound = True
               iColon1Index = sLine.find(':')
               iColon2Index = sLine.find(':', iColon1Index+1)
               if iColon2Index == -1:
                   sID = 'NO_ID'
                   sMessage = sLine[iColon1Index+1:].strip()
               else:
                   sID = sLine[iColon1Index+1:iColon2Index].strip()
                   sMessage = sLine[iColon2Index+1:].strip()
                   if ' ' in sID:
                       sID = 'NO_ID'
                       sMessage = sLine[iColon1Index+1:].strip()
               oWarning = warning.create(sID, sMessage, None, iLineNumber + 1)
       return oReturn

