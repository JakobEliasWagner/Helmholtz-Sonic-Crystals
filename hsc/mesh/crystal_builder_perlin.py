from typing import List

import numpy as np
from scipy.interpolate import splev, splprep
from skimage import measure

from hsc.domain_properties import Description
from hsc.noise import LimitedPerlin

from .crystal_builder import CrystalBuilder


class PerlinCrystalBuilder(CrystalBuilder):
    def __init__(self, description: Description):
        super().__init__(description)

        # define center of crystals
        offset = self.crystal_description.grid_size / 2.0
        self.centers_x = [
            offset + col * self.crystal_description.grid_size + self.box.x_min
            for col in range(self.crystal_description.n)
        ]
        self.center_y = offset + self.box.y_min

        # perlin noise setup
        self.noise = LimitedPerlin(
            n=list(
                range(
                    self.description.crystal.n_min, self.description.crystal.n_min + 1
                )
            ),
            smoothing_steps=self.description.crystal.smoothing_steps,
        )
        self.x = np.linspace(-1, 1, self.description.crystal.n_perlin_grid)
        self.y = np.linspace(-1, 1, self.description.crystal.n_perlin_grid)
        self.n_grid = self.description.crystal.n_perlin_grid
        self.xx, self.yy = np.meshgrid(self.x, self.y)
        self.points = np.stack([self.xx.flatten(), self.yy.flatten()], axis=1)

    def define_objects(self) -> List[int]:
        """Defines disks associated with this type of crystal.

        Returns:
            indices to the surfaces of the disks.
        """
        f = self.noise(self.points)
        self.description.crystal.noise_grid = f

        # find contours
        contours = measure.find_contours(f, 0.0, fully_connected="low")
        contour_coords = []
        for contour in contours:
            upper = np.ceil(contour).astype(int)
            lower = np.floor(contour).astype(int)

            dist_x = contour[:, 0] - lower[:, 0]
            exact_x = self.x[lower[:, 0]] * (1 - dist_x) + self.x[upper[:, 0]] * dist_x

            dist_y = contour[:, 1] - lower[:, 1]
            exact_y = self.y[lower[:, 1]] * (1 - dist_y) + self.y[upper[:, 1]] * dist_y

            contour_coords.append(np.stack([exact_x, exact_y], axis=1))

        crystals = []
        for center_x in self.centers_x:
            crystal = []
            for contour in contour_coords:
                if contour.shape[0] <= 10:
                    continue
                tck, u = splprep([contour[:, 0], contour[:, 1]], s=0.01, per=True)
                u_new = np.linspace(0, 1, contour.shape[0])
                smooth_contour = splev(u_new, tck)

                g_points = []
                for px, py in zip(smooth_contour[0], smooth_contour[1]):
                    px = px * self.description.crystal.grid_size / 2
                    py = py * self.description.crystal.grid_size / 2
                    g_points.append(
                        self.factory.add_point(px + center_x, py + self.center_y, 0.0)
                    )

                lines = [self.factory.add_bspline(g_points + [g_points[0]])]
                loop = self.factory.add_curve_loop(lines)

                crystal.append(self.factory.add_plane_surface([loop]))
            if len(crystal) < 2:
                crystals.append(crystal[0])
                continue
            surfs, _ = self.factory.fuse(
                [(2, crystal[0])], [(2, crs) for crs in crystal[1:]]
            )
            crystals.extend([s[1] for s in surfs])
        return crystals
