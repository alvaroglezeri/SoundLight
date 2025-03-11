from abc import ABC, abstractmethod

from src.core.lightGroups import Group


class IFeature(ABC):
    """
    WRITE
    """
    # def generate(self, generator: IFeatureExporter) -> str:
    #    return generator.generate(self)
    pass


# ----- FEATURES -----

class SimpleFlash(IFeature):
    """
    Simple front light flash.
    """

    def __init__(self, start: float, duration: float, group: Group):
        self.start = start
        self.duration = duration
        self.group = group
        pass

    def __str__(self) -> str:
        return f'SimpleFlash (start: {self.start}, duration: {self.duration}, group: {self.group})'


class OtherFeature(IFeature):
    """
    Another feature to generate
    """

    def __init__(self):
        pass

    def __str__(self):
        return f'Other Feature'
