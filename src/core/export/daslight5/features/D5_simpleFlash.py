from core.generation.featureGenerator import IFeatureExporter
from core.model.features import IFeature


class D5_SimpleFlash(IFeatureExporter):
    """
    Export generator  for SimpleFlash
    """

    def generate(self, feature: IFeature) -> str:

        return ""
