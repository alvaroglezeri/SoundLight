from typing import List
from lxml.etree import _Element as XMLElement
import uuid

from ....export.daslight5.Daslight5Exporter import create_element
from ....model.features import IFeature, IFeatureExporter, SimpleFlash
from .....lib.helpers import get_rand_color


class D5_SimpleFlash(IFeatureExporter):
    """
    Export generator for SimpleFlash.
    The data for the fixtures is obtained directly from hand-crafted scenes.
    """

    # Fixture DATA
    _DATA = {
        'on': "eJxiYGT4z8DAwLiHARu0AWIGAAAAAP//",
        'off': "eJxiYPz/n4GBgXEPAy7IAAAAAP//"
    }

    # Stores the SCENEUID for each scene
    _SCENES = {
        'all': "",
        'even': "",
        'odd': ""
    }

    def generate_scenes(self, feature: type[IFeature], data=None) -> List[XMLElement]:
        """Generates the SCENE element for a SimpleFlash.

        Args:
            feature (IFeature): Feature type for which to generate the scene.
            data (XMLElement, optional): Data required to perform the operation.

        Raises:
            ValueError: If either the data or the feature is invalid.

        Returns:
            List[XMLElement]: List of scenes required to represent the feature.
        """
        # if isinstance(feature, SimpleFlash) or ...
        scenes: List[XMLElement] = []
        if feature is SimpleFlash:
            if isinstance(data, XMLElement):
                for mode in self._SCENES.keys():
                    scene: XMLElement = self._scenes(mode, feature, data)
                    scenes.append(scene)
            else:
                raise ValueError(f'Invalid data type: {type(data)}')

            return scenes
        else:
            raise ValueError(f"Invalid feature type: {feature}")

    # --------------------------------------------------------------------------

    def _scenes(self, mode: str, feature: type[SimpleFlash], data: XMLElement) -> XMLElement:
        """Generates the individual SCENE element for this feature.
        """
        scene: XMLElement = create_element("SCENE")

        # Scene UUID, needed for _fixtureDatas
        self._SCENES[mode] = str(uuid.uuid4())  # Useful for later
        scene.set("DASUID", self._SCENES[mode])
        scene.set("NAME", f"{feature.get_feature_name()} - {mode} (scene)")
        scene.set("COLOR", get_rand_color())
        scene.set("ENABLE", "1")
        scene.set("VISIBLE", "1")
        scene.set("LOOP_MODE", "0")
        scene.set("LOOP", "0")
        scene.set("PLAY_DIRECTION", "1")
        scene.set("PLAY_MODE", "0")
        scene.set("FLASH", "0")
        scene.set("BOUNCE_MODE", "0")
        scene.set("PLAY_TRIGGER", "0")
        scene.set("PLAY_DIVISION", "8")
        scene.set("DIMMER", "1")
        scene.set("D_FEATURE", "1")
        scene.set("SPEED", "0.5")
        scene.set("PHASE", "0")
        scene.set("SIZE", "1")
        scene.set("AUTO_RELEASE_END", "1")
        scene.set("JUMP_MODE", "-1")
        scene.set("RELEASE_MODE", "2")
        scene.set("RELEASE_PROTECT_MODE", "0")
        scene.set("FADE_IN", "0")
        scene.set("FADE_OUT", "7")
        scene.set("ATTRIBUTEVALUE_MODE", "0")
        scene.set("LTPPRIORITY", "2")
        scene.set("PAUSE", "0")
        scene.set("SAIMAGEPATH", "")

        scene.append(self._fixture_datas(mode, feature, data))
        # RACKS element ignored, because these are simple scenes.
        # scene.append(self._rack(...))

        return scene

    def _fixture_datas(self, mode: str, feature: type[SimpleFlash], data: XMLElement) -> XMLElement:
        """Sets the fixtures' DATA attribute to the correct B64 string.
        """
        fixtureDatas: XMLElement = create_element("FIXTUREDATAS")

        # Getting all relevant fixtures in the patch
        fixtures: list = data.xpath(
            f'/DLMFILE/FIXTUREGROUPS/FIXTUREGROUP[@NAME="ParCan"]/FIXTURE/@DASUID'
        )

        fixtureDatas.set("NB", str(len(fixtures)))

        # We select the values, depending on the mode
        match mode:
            case 'all':
                for f in fixtures:
                    attribs = {
                        "FIXTURE": str(f),
                        "DATA": self._DATA['on'],
                    }
                    fixtureDatas.append(create_element("FIXTUREDATA", attribs))
            case 'even':
                on = True
                for f in fixtures:
                    if on:
                        attribs = {
                            "FIXTURE": str(f),
                            "DATA": self._DATA['on'],
                        }
                    else:
                        attribs = {
                            "FIXTURE": str(f),
                            "DATA": self._DATA['off'],
                        }
                    fixtureDatas.append(
                        create_element("FIXTUREDATA", attribs))
                    on = not on

            case 'odd':
                on = False
                for f in fixtures:
                    if on:
                        attribs = {
                            "FIXTURE": str(f),
                            "DATA": self._DATA['on'],
                        }
                    else:
                        attribs = {
                            "FIXTURE": str(f),
                            "DATA": self._DATA['off'],
                        }
                    fixtureDatas.append(
                        create_element("FIXTUREDATA", attribs))
                    on = not on

        return fixtureDatas

    # --------------------------------------------------------------------------

    def generate_instance(self, feature: IFeature, data=None) -> XMLElement:
        """Creates a timeline BLOCK element representing the instance

        Args:
            feature (IFeature): Instance for which to generate the block.
            data (_type_, optional): Not required.

        Raises:
            ValueError: If the feature is invalid.

        Returns:
            XMLElement: BLOCK element for this feature instance.
        """
        if isinstance(feature, SimpleFlash):
            block: XMLElement = create_element("BLOCK")

            block.set("TYPE", "1")
            block.set("DASUID", str(uuid.uuid4()))
            block.set("NAME", feature.get_feature_name())
            block.set("START", str(feature.get_timestamp()))
            block.set("END", str(
                feature.get_timestamp() + feature.get_duration()))
            block.set("POSITION", "0")
            block.set("FADEIN", "0")
            # TODO: BPM calculation?
            block.set("FADEOUT", "600")
            block.set("SPEED", "1")
            block.set("ALLOWLOOP", "1")
            block.set("CONFORM_TO_TEMPO", "1")
            block.set("SCENEUUID", self._SCENES[feature.mode()])

            block.append(create_element('DASTLSUBLINES', {'DASTLNB': '0'}))

            return block
        else:
            raise ValueError(f'Invalid feature type: {feature}')
