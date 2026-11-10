

class ElfwsError(Exception):
    '''
    An error which stops ELFWS.

    The message is printed and ELFWS exits with the exit code.
    '''

    def __init__(self, sMessage, iExitCode):
        super().__init__(sMessage)
        self.iExitCode = iExitCode
