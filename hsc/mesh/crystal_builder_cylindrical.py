from typing import List

from hsc.domain_properties import Description

from .crystal_builder import CrystalBuilder


class CylindricalCrystalBuilder(CrystalBuilder):
    def __init__(self, description: Description):
        super().__init__(description)

        # define center of crystals
        offset = self.crystal_description.grid_size / 2.0
        self.centers_x = [
            offset + col * self.crystal_description.grid_size + self.box.x_min
            for col in range(self.crystal_description.n)
        ]
        self.center_y = offset + self.box.y_min

    def define_objects(self) -> List[int]:
        """Defines disks associated with this type of crystal.

        Returns:
            indices to the surfaces of the disks.
        """
        crystals = []

        for center_x in self.centers_x:
            crystals.append(
                self.factory.addDisk(
                    center_x,
                    self.center_y,
                    0.0,
                    self.crystal_description.radius,
                    self.crystal_description.radius,
                )
            )

        return crystals
