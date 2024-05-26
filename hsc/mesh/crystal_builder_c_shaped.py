from typing import List

from .crystal_builder_cylindrical import CylindricalCrystalBuilder


class CShapedCrystalBuilder(CylindricalCrystalBuilder):
    """C-shaped crystal builder.

    C-shaped sonic crystals use cylindrical shaped crystal as a precursor. The difference to a cylindrical shaped
    crystal is that a slot and a disk are cut from the disk.
    """

    def define_tools(self) -> List[int]:
        """Define slot and disc that needs to be cut from the disk.

        Returns:
            indices to both rectangles and discs used as tools in the cutting operation.
        """
        tools = []

        # inner radius and gap in terms of the outer radius
        inner_radius = self.crystal_description.inner_radius
        # gaps should be smaller than inner radius
        gap_height = self.crystal_description.gap_width
        tol = 1.1  # to prevent cutting artifacts
        gap_width = self.crystal_description.radius * tol

        for center_x in self.centers_x:
            inner_disk = self.factory.addDisk(
                center_x, self.center_y, 0, inner_radius, inner_radius
            )

            slot = self.factory.addRectangle(
                center_x - self.crystal_description.radius * tol,
                self.center_y - gap_height / 2,
                0,
                gap_width,
                gap_height,
            )

            tools.extend([inner_disk, slot])

        return tools
