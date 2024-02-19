import configparser
import pathlib

import numpy as np
import pytest

import hsc.domain_properties as d
from hsc.domain_properties.file_input import read_absorber_config


def test_file_input_domain_general(templates_path):
    for file in ["domain_c_shaped.ini", "domain_cylindrical.ini", "domain_none.ini"]:
        template = templates_path.joinpath(file)
        des = d.read_config(template)[0]

        assert all(
            np.in1d(des.frequencies, np.linspace(4000, 20000, 10))[
                : len(des.frequencies)
            ]
        )
        assert des.rho == 1.2
        assert des.c == 343.0
        c = des.crystal
        assert c.grid_size == 22e-3
        assert c.n == 10


def test_file_input_domain_c_shaped(templates_path):
    template = templates_path.joinpath("domain_c_shaped.ini")
    descriptions = d.read_config(template)
    crystals = [des.crystal for des in descriptions]

    outer_rs = [c.radius for c in crystals]
    inner_rs = [c.inner_radius for c in crystals]
    gap_ws = [c.gap_width for c in crystals]

    assert len(outer_rs) == len(inner_rs)
    assert len(outer_rs) == len(gap_ws)

    assert len(set(outer_rs)) == 2
    assert len(set(inner_rs)) == 4
    assert len(set(gap_ws)) == 8

    assert set(outer_rs) == set(np.linspace(6.5e-3, 9e-3, 2))
    assert set(inner_rs) == set(np.outer(outer_rs, np.linspace(0.7, 0.9, 2)).flatten())
    assert set(gap_ws) == set(np.outer(inner_rs, np.linspace(0.3, 1.0, 2)).flatten())


def test_file_input_domain_cylindrical(templates_path):
    template = templates_path.joinpath("domain_cylindrical.ini")
    descriptions = d.read_config(template)
    crystals = [des.crystal for des in descriptions]

    rs = np.array(list({c.radius for c in crystals}))

    assert len(set(rs)) == 5

    rs.sort()

    assert np.allclose(rs, np.linspace(6.5e-3, 10e-3, 5))


def test_file_input_domain_none(templates_path):
    template = templates_path.joinpath("domain_none.ini")
    descriptions = d.read_config(template)
    crystals = [des.crystal for des in descriptions]

    assert len(crystals) == 9


def test_unknown_crystal_type():
    template = pathlib.Path(__file__).parent.joinpath("domain_wrong_crystal_type.ini")
    with pytest.raises(TypeError):
        d.read_config(template)


def test_wrong_absorber():
    template = pathlib.Path(__file__).parent.joinpath("domain_wrong_absorber_type.ini")
    config = configparser.ConfigParser()
    config.read(template)
    with pytest.raises(TypeError):
        read_absorber_config(config, 1e-3)
