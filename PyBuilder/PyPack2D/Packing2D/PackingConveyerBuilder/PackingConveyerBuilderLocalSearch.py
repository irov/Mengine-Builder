__author__ = 'human88998999877'
from PyBuilder.PyPack2D.Packing2D.PackingConveyer.Accumulator import Accumulator
from PyBuilder.PyPack2D.Packing2D.PackingConveyer.Sorter import Sorter
from PyBuilder.PyPack2D.Packing2D.PackingConveyer.PackingControl.PackingControlLocalSearch import PackingControlLocalSearch
from PyBuilder.PyPack2D.Packing2D.PackingConveyerBuilder.PackingConveyerBuilder import PackingConveyerBuilder


class PackingConveyerBuilderLocalSearch(PackingConveyerBuilder):
    def _onBuild(self, conveyer, factory, settings):
        accumulator = Accumulator()
        conveyer.pushUnit( accumulator )

        if settings.sortOrder is not None:
            sorting = factory.getInstance(settings.sortKey)
            sorter = Sorter(sorting, settings.sortOrder)
            conveyer.pushUnit( sorter )
            pass

        packer = factory.createInstance(settings.packingAlgorithm)
        control = PackingControlLocalSearch(packer, factory, settings)
        conveyer.pushUnit(control)
        pass
    pass
