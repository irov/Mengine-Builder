from PyBuilder.Operation.OperationFactory import OperationFactory
from PyBuilder.Operation.Operation import Operation
from PyBuilder.Error.ErrorHandler import ErrorHandler



class OperationChain(Operation):
    class OperationSource(object):
        def __init__(self, name, **params):
            super(OperationChain.OperationSource, self).__init__()
            self.name = name
            self.params = params
            pass
        pass

    def __init__(self):
        super(OperationChain, self).__init__()
        self.operations = []
        pass

    def _onParams(self, params):
        self.name = params.pop("Name", None)
        self.AutoRun = params.pop("AutoRun", True)
        pass

    def __enter__(self):
        return self
        pass

    def __exit__(self, type, value, traceback):
        if type is not None:
            return False

        if len(self.operations) == 0:
            ErrorHandler.error( "OperationChain.__enter__  operations empty name: %s" % self.name )
            return

        if self.AutoRun is True:
            if self.run() is False:
                raise RuntimeError("OperationChain.__enter__  run is False name: %s self: %s" % (self.name, self))
            pass
        pass

    def addOperation(self, name, **params):
        operationSource = OperationChain.OperationSource( name, **params )
        self.operations.append(operationSource)
        pass

    def _onRun(self):
        for operationSource in self.operations:
            operation = OperationFactory.getOperation(operationSource.name, operationSource.params)
            if operation.run() is False:
                ErrorHandler.warning("invalid chain operation [%s] [%s]", self.__repr__(), operation)
                return False
                pass
            pass

        return True
        pass
    pass
