__author__ = 'human88998999877'
from Builder.Pack2D.Packing2D.PackingConveyer.Accumulator import Accumulator
from Builder.Pack2D.Packing2D.PackingConveyer.Sorter import Sorter
from Builder.Pack2D.Packing2D.PackingConveyer.PackingControl.PackingControl import PackingControl
from Builder.Pack2D.Packing2D.PackingConveyerBuilder.PackingConveyerBuilder import PackingConveyerBuilder

class PackingConveyerBuilderOffline(PackingConveyerBuilder):
    def _onBuild(self, conveyer, factory, settings):
        accumulator = Accumulator()
        conveyer.pushUnit(accumulator)

        if settings.sortOrder is not None:
            sorting = factory.getInstance(settings.sortKey)
            sorter = Sorter(sorting, settings.sortOrder)
            conveyer.pushUnit( sorter )
            pass

        packer = factory.getInstance(settings.packingAlgorithm)
        control = PackingControl(packer, factory, settings)
        conveyer.pushUnit(control)
        pass
    pass
