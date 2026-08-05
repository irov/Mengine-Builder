__author__ = 'human88998999877'
from PyBuilder.PyPack2D.Packing2D.PackingConveyer.Unit import Unit
from PyBuilder.PyPack2D.Packing2D.PackingConveyer.Signal import SignalType,Signal

def getLowPow2( x ):
    y = 2
    if y >= x:
        return None
    while True:
        if y >= x:
            return y / 2
            pass
        y *= 2
        pass
    pass

class PackingControl(Unit):
    def _onInit(self, packer, factory, settings):
        self.packer = packer
        self.packer.initialise(factory, settings)
        self.packer.setSize(settings.maxWidth, settings.maxHeight)

        self.result = []

        self.connect(SignalType.PUSH_INPUT, self._onPushInput)
        self.connect(SignalType.PREPARE_TO_PACK, self._onPrepareToPack)
        self.connect(SignalType.START_PACK, self._onStartPack)
        pass

    def packBins(self, bins):
        # self.lastPack  = False
        # index = 0
        bins_black = bins[:]
        bins_white = []

        while True:
            for bin in bins_black:
                if self.packer.packBin(bin) is True:
                    continue
                    pass

                bins_white.append(bin)
                pass

            set = self.packer.flush()
            self.result.append(set)

            if len(bins_white) == 0:
                break
                pass

            bins_black = bins_white[:]
            bins_white = []
            pass
        pass

    def _onPushInput(self, input):
        self.packBins(input)
        return True
        pass

    def _onStartPack(self, dummy):
        #TODO REFACTOR
        self.processSignal( Signal(SignalType.END_PACK, self.result) )
        return True
        pass

    def _onPrepareToPack(self, dummy):
        self.processSignal( Signal(SignalType.CREATE_PACKER, self.packer) )
        self.result = []
        return True
        pass
    pass
