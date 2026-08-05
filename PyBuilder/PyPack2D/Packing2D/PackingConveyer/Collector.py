__author__ = 'human88998999877'
from PyBuilder.PyPack2D.Packing2D.PackingConveyer.Unit import Unit,checkUnitForwardLinkDoesNotExist
from PyBuilder.PyPack2D.Packing2D.PackingConveyer.Signal import SignalType

class Collector(Unit):
    def _onInit(self):
        self.connect(SignalType.END_PACK, self._onEndToPack)
        self.connect(SignalType.WASTE_INPUT, self._onWasteInput)
        self.result = None
        self.waste = []
        pass

    @checkUnitForwardLinkDoesNotExist
    def _onEndToPack(self, result):
        self.result = result
        return True
        pass

    def _onWasteInput(self, waste):
        self.waste.extend(waste)
        return True
        pass

    def getResult(self):
        return self.result
        pass

    def getWaste(self):
        return self.waste
        pass
    pass
