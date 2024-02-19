import gmsh

from hsc.mesh import (CrystalBuilder, CShapedCrystalBuilder,
                      CylindricalCrystalBuilder)


def test_base_crystal_builder_empty(descriptions):
    for description in descriptions:
        cb = CrystalBuilder(description)
        assert len(cb.build()) == 0


def test_cylindrical_builder(cylindrical_descriptions):
    description = cylindrical_descriptions[0]
    cb = CylindricalCrystalBuilder(description)
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)
    gmsh.model.add("test_cylindrical_builder")
    n_cylinders = description.crystal.n
    assert len(cb.build()) == n_cylinders
    gmsh.finalize()


def test_c_shaped_builder(c_shaped_descriptions):
    description = c_shaped_descriptions[0]
    cb = CShapedCrystalBuilder(description)
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)
    gmsh.model.add("test_c_shaped_builder")
    n_cylinders = description.crystal.n
    assert len(cb.build()) == n_cylinders
    gmsh.finalize()
