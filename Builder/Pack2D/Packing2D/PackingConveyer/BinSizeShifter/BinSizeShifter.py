from Builder.Pack2D.Packing2D.PackingConveyer.Unit import Unit
from Builder.Pack2D.Packing2D.PackingConveyer.Signal import SignalType

class BinSizeShifter(Unit):
    def _onInit(self):
        self.connect(SignalType.END_PACK, self._onEndToPack)
        self.connect(SignalType.CREATE_PACKER, self._onCreatePacker)
        pass

    def shift(self, binSet):
        self._onShift(binSet)
        pass

    def _onCreatePacker(self, packer):
        self.packer = packer
        return True
        pass

    def _onEndToPack(self, result):
        for binSet in result:
            self.shift(binSet)
            pass

        return True
        pass

    def _onShift(self, binSet):
        raise NotImplementedError()
        pass
    pass
