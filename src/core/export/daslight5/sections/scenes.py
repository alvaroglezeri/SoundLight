import itertools
import json
from typing import List
import uuid
from lxml.etree import _Element as XMLElement

from ....export.daslight5.Daslight5Exporter import create_element, Section
from ....export.daslight5.features.D5_featureCreator import D5FeatureCreator
from ....model.features import FeatureSerializer, IFeature
from ....model.song import Song
from .....lib.helpers import get_rand_color


class Scenes(Section):
    """SCENES element in the DLM file.
    """

    def __init__(self, dlmfile: XMLElement):
        self.dlmFile = dlmfile
        self._featureCreator = D5FeatureCreator(self.dlmFile)
        self._featureSerializer = FeatureSerializer

    # --------------------------------------------------------------------------

    def write(self, song: Song) -> XMLElement:
        """Crafts the XMLElement SCENES, for the .dvc file.

        Args:
            song (Song): Song for which to create the configuration.
        """
        self._song = song
        ret: XMLElement = create_element("SCENES")

        # Classify features per type.
        self._classified_features: dict = {}
        for f in song['features']:
            if type(f) not in self._classified_features:
                self._classified_features[type(f)] = []
            self._classified_features[type(f)].append(f)

        # Banks with the scenes, one bank per feature
        for feature_class, _ in self._classified_features.items():
            ret.append(self._feature_type_bank(feature_class))

        # SuperScene bank
        ret.insert(0, self._superscene_bank())

        # DAS_SELECTIONS
        ret.append(create_element('DAS_SELECTIONS',
                   {'SELECTED_LIVE_BANK': '1'}))

        return ret

    # --------------------------------------------------------------------------

    def _feature_type_bank(self, feature_class: IFeature) -> XMLElement:
        """BANK element for this feature class, can create more than one scene.
        """
        bank: XMLElement = create_element("BANK")

        bank.set("DASUID", str(uuid.uuid4()))
        bank.set("NAME", feature_class.get_feature_name())
        bank.set("COLOR", get_rand_color())
        bank.set("COLLAPSED", "0")
        bank.set("PAUSED", "0")
        bank.set("HIDDEN", "0")
        bank.set("NBSCENE", "1")

        featureType_scenes = self._feature_type_scene(feature_class)
        if isinstance(featureType_scenes, list):
            for scene in featureType_scenes:
                bank.append(scene)
        else:
            bank.append(featureType_scenes)

        return bank

    # --------------------------------------------------------------------------

    def _feature_type_scene(self, feature_class: IFeature) -> List[XMLElement]:
        return self._featureCreator.create_scenes_for(feature_class)

    # --------------------------------------------------------------------------

    def _superscene_bank(self) -> XMLElement:
        """The superscene holds the timeline of features, arranged at the correct time.
        It is contained in its own bank, as it is not directly related with one single feature.
        """
        superscene: XMLElement = create_element("BANK")

        superscene.set("DASUID", str(uuid.uuid4()))
        superscene.set("NAME", "SuperScene")
        superscene.set("COLOR", get_rand_color())
        superscene.set("COLLAPSED", "0")
        superscene.set("PAUSED", "0")
        superscene.set("HIDDEN", "0")
        superscene.set("NBSCENE", "1")

        superscene.append(self._superscene_scene())

        return superscene

    # --------------------------------------------------------------------------

    def _superscene_scene(self) -> XMLElement:
        """SCENE element and its attributes. COuld be loaded from the configuration, but default values work fine.
        """
        scene: XMLElement = create_element("SCENE")

        scene.set("DASUID", str(uuid.uuid4()))
        scene.set("NAME", "Timeline")
        scene.set("COLOR", get_rand_color())
        scene.set("ENABLE", "1")
        scene.set("VISIBLE", "1")
        scene.set("LOOP_MODE", "1")
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
        scene.set("FADE_OUT", "0")
        scene.set("ATTRIBUTEVALUE_MODE", "0")
        scene.set("LTPPRIORITY", "2")
        scene.set("PAUSE", "0")
        scene.set("SAIMAGEPATH", "")

        scene.append(create_element("FIXTUREDATAS", {"NB": "0"}))
        scene.append(self._superscene_rack())

        return scene

    # --------------------------------------------------------------------------

    def _superscene_rack(self) -> XMLElement:
        """Inside the scene, the rack contains the timelines.
        """
        racks: XMLElement = create_element('RACKS')
        rack: XMLElement = create_element('RACK')

        rack.set('TYPE', '1')
        # Can be ignored to auto-calculate
        # rack.set('DURATION', str('?'))
        rack.set('DISPLAY_MODE', '1')
        rack.set('GRID_BPM', str(self._song['metadata']['deeprythm']['bpm']))
        # rack.set('GRID_BPM', str(self._song['song']['bpm']))
        rack.set('GRID_OFFSET', '0')

        timelines: XMLElement = create_element('TIMELINES')
        timelines.append(self._track_timeline())

        for timeline in self._feature_timelines():
            timelines.append(timeline)

        rack.append(timelines)

        racks.append(rack)
        return racks

    # --------------------------------------------------------------------------

    def _track_timeline(self) -> XMLElement:
        """Creates the track that contains the song file. Nothing else is stored here.

        Returns:
            XMLElement: _description_
        """
        timeline: XMLElement = create_element('TIMELINE')

        timeline.set('DASUID', str(uuid.uuid4()))
        timeline.set('NAME', 'Track')
        timeline.set('INDEX', '0')
        timeline.set('DASTLLOCKED', '1')
        timeline.set('DASTLMUTED', '0')
        timeline.set('DASTLFOLDED', '1')

        blocks: XMLElement = create_element('BLOCKS')
        block: XMLElement = create_element('BLOCK')

        block.set('TYPE', '2')
        block.set('DASUID', str(uuid.uuid4()))
        block.set('NAME', self._song['title'])
        block.set('START', '0')
        duration = str(int(self._song['metadata']
                       ['tinytag']['duration'] * 1000))
        block.set('END', duration)
        block.set('POSITION', '0')
        block.set('FADEIN', '0')
        block.set('FADEOUT', '0')
        # Loading the path of the song. This is the actual song path, and must coincide with its location.
        block.set('DASTLMEDIAPATH', self._song['path'])
        block.set('DASTLHEIGHT', '1')
        block.set('BPM', str(self._song['metadata']['deeprythm']['bpm']))
        block.set('ALLOWLOOP', '1')
        block.set('CONFORM_TO_TEMPO', '1')

        block.append(create_element('DASTLSUBLINES', {'DASTLNB': '0'}))
        blocks.append(block)
        timeline.append(blocks)
        return timeline

    # --------------------------------------------------------------------------

    def _feature_timelines(self) -> List[XMLElement]:
        """Timelines for the features, one timeline for each feature type.
        """
        timelines: list = []
        self._feat_types: dict

        i = 1
        feature_class: IFeature
        features: List[IFeature]

        for feature_class, features in self._classified_features.items():
            timeline: XMLElement = create_element('TIMELINE')

            timeline.set('DASUID', str(uuid.uuid4()))
            timeline.set('NAME', feature_class.get_feature_name())
            timeline.set('INDEX', str(i))
            i += 1
            timeline.set('DASTLLOCKED', '0')
            timeline.set('DASTLMUTED', '0')
            timeline.set('DASTLFOLDED', '1')

            blocks: XMLElement = create_element('BLOCKS')

            for f in features:
                blocks.append(self._feature_timeline_block(f))

            timeline.append(blocks)
            timelines.append(timeline)
        return timelines

    # --------------------------------------------------------------------------

    def _feature_timeline_block(self, feature: IFeature) -> XMLElement:
        """Creates the block on the timeline for this fixture.

        Args:
            feature (IFeature): Feature instance.
        """
        return self._featureCreator.create_tlblock_for(feature)
