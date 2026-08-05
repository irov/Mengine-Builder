__author__ = 'human88998999877'
from PyBuilder.PyPack2D.Packing2D.PackingConveyer.Validator import Validator
from PyBuilder.PyPack2D.Packing2D import BinSizeMode,RotateMode

class PackingConveyerBuilder(object):
    def build(self, conveyer, factory, settings):
        if settings.rotateMode == RotateMode.UP_RIGHT or settings.rotateMode == RotateMode.SIDE_WAYS:
            rotator = factory.getInstance(settings.rotateMode)
            conveyer.pushUnit(rotator)
            pass

        validator = Validator( settings.maxWidth, settings.maxHeight )
        conveyer.pushUnit(validator)

        self._onBuild(conveyer, factory, settings)
        if settings.binSizeMode == None or settings.binSizeMode == BinSizeMode.STRICT:
            return
            pass

        shifter = factory.getInstance(settings.binSizeMode)
        conveyer.pushUnit(shifter)
        pass

    def _onBuild(self, conveyer, factory, settings):
        pass
    pass
