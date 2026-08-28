__author__ = 'human88998999877'

from Builder.Pack2D.Packing2D.PackingConveyer.Unit import Unit
from Builder.Pack2D.Packing2D.PackingConveyer.Signal import Signal,SignalType

#split input sequence S on groups of sub sequences S1..Sn where  length each of them == count
class Filter(Unit):
    def _onInit(self, count):
        self.count = count
        self.connect(SignalType.PUSH_INPUT, self._onPushInput)
        pass

    def _onPushInput(self, input):
        if self.count <= 0:
            return
            pass

        if self.nextUnit is None:
            return
            pass

        newInput = []
        count = self.count
        for image in input:
            newInput.append(image)
            count -= 1

            if count > 0:
                continue
                pass

            newSignal = Signal(SignalType.PUSH_INPUT, newInput)
            self._processNext(newSignal)

            newInput = []
            count = self.count
            pass

        #return False to stop this signal
        return False
        pass
    pass
