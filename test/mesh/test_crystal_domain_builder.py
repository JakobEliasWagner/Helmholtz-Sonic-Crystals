import gmsh

from hsc.mesh import (
    CrystalDomainBuilder,
    CShapedCrystalDomainBuilder,
    CylindricalCrystalDomainBuilder,
)


def test_cylindrical_crystal_domain_builder(template_cylindrical_descriptions):
    description = template_cylindrical_descriptions[0]
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)
    gmsh.model.add("test cylindrical domain")
    b = CylindricalCrystalDomainBuilder(description)
    assert len(b.build()) == 1
    gmsh.finalize()


def test_c_shaped_crystal_domain_builder(template_c_shaped_descriptions):
    description = template_c_shaped_descriptions[0]
    gmsh.initialize()
    gmsh.model.add("test c-shaped domain")
    gmsh.option.setNumber("General.Verbosity", 0)
    b = CShapedCrystalDomainBuilder(description)
    assert len(b.build()) == 1
    gmsh.finalize()


def test_none_crystal_domain_builder(template_none_descriptions):
    description = template_none_descriptions[0]
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)
    gmsh.model.add("test none domain")
    b = CrystalDomainBuilder(description)
    assert len(b.build()) == 1
    gmsh.finalize()
