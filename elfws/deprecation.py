
import warnings


def build_module_getattr(sModuleName, dDeprecatedNames):
    '''
    Creates a module __getattr__ function which returns deprecated names.

    Accessing a deprecated name issues a DeprecationWarning and returns
    the object which replaces it.

    Parameters:

      sModuleName : (string) name of the module, used in messages

      dDeprecatedNames : (dictionary) deprecated name to replacement object

    Returns: (function)
    '''
    def module_getattr(sName):
        if not is_deprecated_name(sName, dDeprecatedNames):
            raise AttributeError('module ' + repr(sModuleName) + ' has no attribute ' + repr(sName))
        warn_deprecated_name(sModuleName, sName, dDeprecatedNames[sName])
        return dDeprecatedNames[sName]

    return module_getattr


def warn_deprecated_name(sModuleName, sName, oReplacement):
    sShortModuleName = sModuleName.split('.')[-1]
    sOld = sShortModuleName + '.' + sName
    sNew = sShortModuleName + '.' + oReplacement.__name__
    warnings.warn(sOld + ' is deprecated and will be removed in a future release, use ' + sNew + ' instead.', DeprecationWarning, stacklevel=3)


def is_deprecated_name(sName, dDeprecatedNames):
    return sName in dDeprecatedNames
