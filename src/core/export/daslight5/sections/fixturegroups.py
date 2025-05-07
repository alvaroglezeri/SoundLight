from lxml.etree import _Element as XMLElement
import uuid

from core.model.song import Song
from core.export.daslight5.Daslight5Creator import createElement, Section


class FixtureGroups(Section):

    def __init__(self, dlmfile: XMLElement):
        self.dlmfile = dlmfile

    def write(self, song: Song) -> XMLElement:
        """
        WRITE
        """
        ret: XMLElement = createElement('FIXTUREGROUPS')

        # TODO: Load data from lightGroups:
        # As of now, and as the groups are only useful for the user, create groups based on the fixture type
        # The first group is always All:

        data: dict = song.metadata

        ret.append(self._groupAll(data['patch']))

        group: str
        for group in data['patch']['fixtureTypes']:
            group_data: dict = data['patch']['fixtureTypes'][group]
            ret.append(self._fixtureGroup(group, group_data))

        return ret

    def _groupAll(self, data: dict) -> XMLElement:
        all: XMLElement = createElement('FIXTUREGROUP')

        group_uuid: str = str(uuid.uuid4())
        data['AllDasUID'] = group_uuid

        all.set('DASUID', group_uuid)
        all.set('NAME', 'All')

        # Default values:
        all.set('TOGGLE_BLACKOUT', str(0))
        all.set('TOGGLE_STROBE', str(0))
        all.set('TOGGLE_FULL', str(0))
        all.set('TOGGLE_EXCLUSIVE_FULL', str(0))
        all.set('TOGGLE_FLASH', str(0))
        all.set('TOGGLE_EXCLUSIVE_FLASH', str(0))

        for fixtureType_name in data['fixtureTypes']:
            for fixture in data['fixtureTypes'][fixtureType_name]['fixtures']:
                f: XMLElement = createElement('FIXTURE')
                f.set('DASUID', fixture['DasUID'])

                all.append(f)

        return all

    def _fixtureGroup(self, group_name: str, group_data: dict) -> XMLElement:
        fixtureGroup: XMLElement = createElement('FIXTUREGROUP')

        group_uuid: str = str(uuid.uuid4())
        group_data['DasUID'] = group_uuid

        fixtureGroup.set('DASUID', group_uuid)
        fixtureGroup.set('NAME', group_name)

        # Default values:
        fixtureGroup.set('TOGGLE_BLACKOUT', str(0))
        fixtureGroup.set('TOGGLE_STROBE', str(0))
        fixtureGroup.set('TOGGLE_FULL', str(0))
        fixtureGroup.set('TOGGLE_EXCLUSIVE_FULL', str(0))
        fixtureGroup.set('TOGGLE_FLASH', str(0))
        fixtureGroup.set('TOGGLE_EXCLUSIVE_FLASH', str(0))

        for fixture in group_data["fixtures"]:
            f: XMLElement = createElement('FIXTURE')
            f.set('DASUID', fixture['DasUID'])

            fixtureGroup.append(f)

        beamSelection: XMLElement = createElement('BEAMSELECTION')
        fixtureGroup.append(beamSelection)

        return fixtureGroup
