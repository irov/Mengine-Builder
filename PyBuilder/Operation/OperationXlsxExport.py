from PyBuilder.Operation.Operation import Operation
from PyBuilder.Error.ErrorHandler import ErrorHandler

class OperationXlsxExport(Operation):
    def _getInfo(self):
        return  "CodeName  %s" % (self.CodeName)
        pass

    def _onParams(self, params):
        self.CodeName = params.pop("CodeName")
        pass

    def _onRun(self):
        try:
            from PyBuilder.WinregCompat import install_macos_winreg

            install_macos_winreg()

            from xlsxExporter import export
            return export(self.CodeName)
        except ImportError as ex:
            ErrorHandler.error("Error: invalid found xlsxExporter: %s", ex)
            pass

        return False;
        pass
    pass
