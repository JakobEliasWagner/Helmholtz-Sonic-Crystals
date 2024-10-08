from typing import List

from hsc.domain_properties import Description

from .gmsh_builder import GmshBuilder


class CrystalBuilder(GmshBuilder):
    """Base class for crystal builders.

    Crystal builders are used to define all shapes of the crystals placed within a simulation domain. This base class
    does not place any crystals in the domain.
    """

    def __init__(self, description: Description):
        super().__init__(description)
        self.crystal_description = description.crystal
        self.box = self.description.crystal_box

    def build(self) -> List[int]:
        """Builds the crystals according to the domain description.

        Returns:
            indices to all newly created crystals.
        """
        objs = self.define_objects()
        tools = self.define_tools()
        if len(tools) > 0:
            crystals = self.cut(objs, tools)
        else:
            crystals = objs

        return crystals

    def define_objects(self) -> List[int]:
        """Defines the objects associated with constructing the crystal by cutting.

        Returns:
            indices to all objects.
        """
        return []

    def define_tools(self) -> List[int]:
        """Defines the tools associated with constructing the crystal by cutting.

        Returns:
            indices to all tools.
        """
        return []

    def cut(self, objs: List[int], tools: List[int]) -> List[int]:
        """Cuts the tools from the objects.

        Args:
            objs: basic shape of the crystals.
            tools: tools which are removed from the basic shape to create the crystal.

        Returns:
            indices to all crystals.
        """
        tags, _ = self.factory.cut(
            [(2, obj) for obj in objs], [(2, tool) for tool in tools]
        )
        domains = [tag[1] for tag in tags]
        return domains
