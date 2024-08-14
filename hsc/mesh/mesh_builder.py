import pathlib
import re
import warnings
from collections import defaultdict
from typing import List, Tuple

import gmsh
import numpy as np

from hsc.domain_properties import (
    CShapeDescription,
    CylinderDescription,
    Description,
    NoneDescription,
    PerlinDescription,
)

from .crystal_domain_builder import (
    CrystalDomainBuilder,
    CShapedCrystalDomainBuilder,
    CylindricalCrystalDomainBuilder,
    PerlinCrystalDomainBuilder,
)
from .gmsh_builder import GmshBuilder


class MeshBuilder(GmshBuilder):
    def __init__(self, description: Description, out_file: pathlib.Path):
        super().__init__(description)
        self.out_file = out_file

        # set appropriate builders
        if isinstance(description.crystal, CylinderDescription):
            db = CylindricalCrystalDomainBuilder
        elif isinstance(description.crystal, CShapeDescription):
            db = CShapedCrystalDomainBuilder
        elif isinstance(description.crystal, NoneDescription):
            db = CrystalDomainBuilder
        elif isinstance(description.crystal, PerlinDescription):
            db = PerlinCrystalDomainBuilder
        else:
            warnings.warn(
                f"Unknown crystal type {description.crystal}. Defaulting to None!",
                category=UserWarning,
            )
            db = CrystalDomainBuilder
        self.domain_builder = db(description)

    def build(self):
        try:
            gmsh.initialize()
            gmsh.option.setNumber(
                "General.Verbosity", 1
            )  # set verbosity level (still prints warnings)
            gmsh.model.add(f"model_{self.description.unique_id}")

            self.build_basic_shapes()
            self.fragment_domain()
            groups = self.get_physical_groups()
            self.set_physical_groups(groups)
            self.set_mesh_properties()
            self.generate_mesh()

            self.save_mesh()
            gmsh.finalize()
        except:  # noqa
            # Gmsh throws a general exception on failing the build
            print("Failed to build mesh - restarting build")
            biggest_nbr = 0
            for file in pathlib.Path.cwd().joinpath("failed").iterdir():
                biggest_nbr = max([biggest_nbr, int(re.findall(r"\d+", file.name)[0])])
            pathlib.Path.cwd().joinpath("failed", f"failed_{biggest_nbr}.png").unlink()
            self.build()

    def delete_msh_files(self):
        self.out_file.unlink()

    def set_mesh_properties(self):
        """Sets properties that the meshing algorithm needs."""
        self.factory.synchronize()

        resolution = (
            self.description.c
            / self.description.max_frequency
            / self.description.elements_per_lambda
        )
        curve_resolution = (
            self.description.c
            / self.description.max_frequency
            / self.description.elements_per_lambda_surf
        )

        # curves
        curves = self.factory.get_entities(1)

        # relevant curves
        relevant_curves = []
        for curve in curves:
            com = self.factory.get_center_of_mass(*curve)
            if (
                len(self.description.crystal_box.inside(np.array(com).reshape(-1, 1)))
                != 0
            ):
                relevant_curves.append(curve[1])
            elif np.isclose(self.description.crystal_box.x_min, com[0]) or np.isclose(
                self.description.crystal_box.x_max, com[0]
            ):
                relevant_curves.append(curve[1])

        # field
        distance = gmsh.model.mesh.field.add("Distance")
        gmsh.model.mesh.field.setNumbers(distance, "CurvesList", relevant_curves)
        gmsh.model.mesh.field.setNumber(distance, "Sampling", 100)

        threshold = gmsh.model.mesh.field.add("Threshold")
        gmsh.model.mesh.field.setNumber(threshold, "IField", distance)
        gmsh.model.mesh.field.setNumber(threshold, "SizeMin", curve_resolution)
        gmsh.model.mesh.field.setNumber(threshold, "SizeMax", resolution)
        gmsh.model.mesh.field.setNumber(
            threshold, "DistMin", self.description.crystal.grid_size / 20
        )
        gmsh.model.mesh.field.setNumber(
            threshold, "DistMax", self.description.crystal.grid_size / 5
        )

        gmsh.model.mesh.field.setAsBackgroundMesh(threshold)

        gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
        gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
        gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)

        """gmsh.option.setNumber(
            "Mesh.MeshSizeMax",
            resolution
        )"""
        # gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 30)

    def generate_mesh(self):
        """Generates the mesh."""
        self.factory.synchronize()
        gmsh.model.mesh.generate(2)
        gmsh.model.mesh.optimize("Netgen")

    def build_basic_shapes(self) -> List[int]:
        """Builds all basic shapes.

        Basic shapes are rectangles within the domain. However, what is inside these rectangles may vary (i.e., cuts).
        Generates the crystal domain, a left and right space, and absorbers according to the description.

        Returns:
            indices to surfaces of generated shapes.
        """
        tags = []
        # left space, domain, right space
        box = self.description.left_box
        if box.size[0] > 0:
            tags.append(
                self.factory.addRectangle(
                    box.x_min, box.y_min, 0.0, box.size[0], box.size[1]
                )
            )
        tags.append(self.domain_builder.build())
        box = self.description.right_box
        if box.size[0] > 0:
            tags.append(
                self.factory.addRectangle(
                    box.x_min, box.y_min, 0.0, box.size[0], box.size[1]
                )
            )
        # absorbers
        for box in self.description.absorber_boxes.values():
            tags.append(
                self.factory.add_rectangle(
                    box.x_min, box.y_min, 0.0, box.size[0], box.size[1]
                )
            )

        return tags

    def fragment_domain(self) -> List[int]:
        """Fragments all parts of the domain, to create one connected mesh.

        Returns:
            All surface indices in the domain.
        """
        all_surfaces = self.factory.get_entities(2)

        # fragment everything
        new_tags, _ = self.factory.fragment([all_surfaces[0]], all_surfaces[1:])

        return [tag[1] for tag in new_tags]

    def get_physical_groups(self) -> List[Tuple[int, List[int], int]]:
        """Takes the domain and identifies different physical groups.

        Returns:
            Tuples containing the dim, physical tag, and a list of surface tags within this group
        """
        # surface
        all_surfaces = self.factory.get_entities(2)
        surf_categories = defaultdict(list)

        for _, surf in all_surfaces:
            com = np.array(self.factory.getCenterOfMass(2, surf)).reshape(
                (3, 1)
            )  # reshape to use bbox
            # find absorbers by calculating distance to inner box (including crystal domain and right spacer)
            if self.description.left_box.inside(com).size:
                surf_categories["left_side"].append(surf)
                continue
            if self.description.crystal_box.inside(com).size:
                surf_categories["crystal_domain"].append(surf)
                continue
            if self.description.right_box.inside(com).size:
                surf_categories["right_side"].append(surf)
                continue
            surf_categories["absorber"].append(surf)

        categories = []
        for name, indices in surf_categories.items():
            categories.append((2, indices, self.description.indices[name]))

        return categories

    def set_physical_groups(self, groups: List[Tuple[int, List[int], int]]) -> None:
        """Sets physical groups according to the given groups

        Args:
            groups: tuple containing (dim, surface_tags, physical group index)
        """
        self.factory.synchronize()
        for group in groups:
            gmsh.model.add_physical_group(*group)

    def save_mesh(self) -> None:
        """Saves raw mesh with physical groups to file."""
        self.out_file.parent.mkdir(exist_ok=True, parents=True)
        gmsh.write(str(self.out_file))  # gmsh does not accept pathlib path
