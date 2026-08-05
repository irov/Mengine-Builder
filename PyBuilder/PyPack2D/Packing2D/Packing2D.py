__author__ = 'human88998999877'
from PyBuilder.PyPack2D.Packing2D.PackingConveyer.Conveyer import Conveyer
from PyBuilder.PyPack2D.Packing2D import packingFactory

from PyBuilder.PyPack2D.Packing2D.PackingConveyer.Signal import SignalType,Signal

class Packing2D(object):
    def __init__(self):
        super(Packing2D, self).__init__()
        self.conveyer = None

        self.factory = packingFactory
        pass

    def initialise(self, settings):
        self.conveyer = Conveyer()
        builder = self.factory.getInstance(settings.packingMode)
        builder.build(self.conveyer, self.factory, settings)
        signal = Signal(SignalType.PREPARE_TO_PACK, None)
        self.conveyer.processSignal(signal)
        pass

    def pack(self):
        signal = Signal(SignalType.START_PACK, None)
        self.conveyer.processSignal(signal)
        pass

    def getResult(self):
        return self.conveyer.getResult()
        pass

    def getWaste(self):
        return self.conveyer.getWaste()
        pass

    def push(self, input):
        _input = input
        if isinstance(input, list) is False:
            _input = [input]
            pass

        signal = Signal(SignalType.PUSH_INPUT, _input)
        self.conveyer.processSignal(signal)
        pass
    pass
