__author__ = 'human88998999877'
from Builder.Pack2D.Packing2D.PackingConveyer.Unit import Unit,checkUnitForwardLinkExist
from Builder.Pack2D.Packing2D.PackingConveyer.Signal import SignalType
from Builder.Pack2D.Packing2D.PackingConveyer.Collector import Collector


class Conveyer(Unit):
    def _onInit(self):
        self.connect(SignalType.PREPARE_TO_PACK, self._onPrepareToPack)
        self.collector = Collector()
        self.waste = []
        pass

    @checkUnitForwardLinkExist
    def _onPrepareToPack(self, dummy):
        self.pushUnit(self.collector)
        return True
        pass

    def getResult(self):
        return self.collector.getResult()
        pass

    def getWaste(self):
        return self.collector.getWaste()
        pass
    pass
