__author__ = 'human88998999877'
from Builder.Pack2D.Packing2D.PackingConveyer.Unit import Unit,checkUnitForwardLinkExist
from Builder.Pack2D.Packing2D.PackingConveyer.Signal import SignalType,Signal

class Accumulator(Unit):
    def _onInit(self):
        self.connect(SignalType.START_PACK, self._onStartPack)
        self.connect(SignalType.PUSH_INPUT, self._onPushInput)

        self.input = []
        pass

    @checkUnitForwardLinkExist
    def _onStartPack(self, dummy):
        newSignal = Signal(SignalType.PUSH_INPUT, self.input)
        self._processNext(newSignal)
        return True
        pass

    @checkUnitForwardLinkExist
    def _onPushInput(self, input):
        self.input.extend(input)
        #stop diffusion of the  signal
        return False
        pass
    pass
