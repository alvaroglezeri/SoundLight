from lxml.etree import _Element as XMLElement
import uuid

from ....model.song import Song
from ....export.daslight5.Daslight5Exporter import create_element, Section


class FixtureGroups(Section):
    """FIXTUREGROUPS element in the DLM file.
    """

    def __init__(self, dlmfile: XMLElement):
        self.dlmfile = dlmfile

    def write(self, song: Song) -> XMLElement:
        """Crafts the XMLElement FIXTUREGROUPS, for the .dvc file.

        Args:
            song (Song): Song for which to create the configuration.
        """
        ret: XMLElement = create_element('FIXTUREGROUPS')

        # As the groups are only useful for the user, create groups based on the fixture type
        # The first group is always All:

        data: dict = song['patch']

        ret.append(self._fixture_group_all(data))

        group: str
        for group in data['fixtureTypes']:
            group_data: dict = data['fixtureTypes'][group]
            ret.append(self._fixture_group(group, group_data))

        return ret

    def _fixture_group_all(self, data: dict) -> XMLElement:
        """Creates the 'All' group. Required, and should be first.
        """
        all: XMLElement = create_element('FIXTUREGROUP')

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
                f: XMLElement = create_element('FIXTURE')
                f.set('DASUID', fixture['DasUID'])

                all.append(f)

        return all

    def _fixture_group(self, group_name: str, group_data: dict) -> XMLElement:
        """Creates a group.

        Args:
            group_name (str): Name of the 'NAME' attribute for this element.
            group_data (dict): Dict with the info of the group. Should have a 'fixtures' entry, with a list of fixtures.
        """
        fixtureGroup: XMLElement = create_element('FIXTUREGROUP')

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
            f: XMLElement = create_element('FIXTURE')
            f.set('DASUID', fixture['DasUID'])

            fixtureGroup.append(f)

        # Empty section
        beamSelection: XMLElement = create_element('BEAMSELECTION')
        fixtureGroup.append(beamSelection)

        return fixtureGroup
