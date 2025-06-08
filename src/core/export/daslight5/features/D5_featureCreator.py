from typing import List, cast
from lxml.etree import _Element as XMLElement

from core.export.daslight5.features.D5_RotFlash import D5_RotFlash
from core.export.daslight5.features.D5_RGBWFlash import D5_RGBWFlash
from core.export.daslight5.features.D5_simpleFlash import D5_SimpleFlash
from core.model.features import IFeature, IFeatureExporter, RGBWFlash, RotFlash, SimpleFlash


class D5FeatureCreator:
    """As the features from ``core.model.features`` do not know the implementation for each exporter, classes are needed to perform this translation. This class manages thoses 'translators'.
    """

    def __init__(self, dlmFile: XMLElement) -> None:
        """Instantiates the feature creator for Daslight 5.

        Args:
            dlmFile (XMLElement): XML element with the DLM content.
        """
        self._dlmFile = dlmFile

        self._supported: dict[type[IFeature], IFeatureExporter] = {
            SimpleFlash: D5_SimpleFlash(),
            RGBWFlash: D5_RGBWFlash(),
            RotFlash: D5_RotFlash()
        }

    def create_scenes_for(self, feat_type: IFeature) -> List[XMLElement]:
        """Creates the needed scene or scenes for a feature, as some features might need several scenes to be represented.

        Args:
            feat_type (IFeature): Receives a class, not an instance!

        Raises:
            ValueError: When the passed feature is not supported.

        Returns:
            XMLElement: SCENE XMl element(s) for the feature.
        """
        if feat_type in self._supported:
            return list(self._supported[feat_type].generate_scenes(feat_type, self._dlmFile))
        else:
            raise ValueError('This feature is not supported!')

    def create_tlblock_for(self, feature: IFeature) -> XMLElement:
        """Creates the feature's blocks on the timeline.

        Args:
            feature (IFeature): Feature for which to generate blocks.

        Raises:
            ValueError: When the passed feature is not supported.

        Returns:
            XMLElement: BLOCK XML element(s) for the feature
        """
        if type(feature) in self._supported:
            return cast(XMLElement, self._supported[type(feature)].generate_instance(feature, self._dlmFile))
        else:
            raise ValueError('This feature is not supported!')
