import pathlib

import numpy as np
import pytest

import hsc.domain_properties as d


@pytest.fixture(scope="module")
def example_c_domain_file():
    return pathlib.Path.cwd().joinpath("templates", "domain_c_shaped.ini")


@pytest.fixture(scope="module")
def crystal_descriptions():
    return [
        d.CylinderDescription(0.22, 19, 42.42),
        d.CShapeDescription(123.23, 12, 1.22, 0.9, 0.5),
        d.NoneDescription(0.22, 12),
    ]


@pytest.fixture(scope="module")
def absorber_description():
    return d.AdiabaticAbsorberDescription(0.22, 123.23, 123)


@pytest.fixture(scope="module")
def descriptions(absorber_description, crystal_descriptions):
    return [
        d.Description(
            frequencies=np.arange(1, 42),
            rho=1.25,
            c=343.0,
            n_left=0.55,
            n_right=0.55,
            elements_per_lambda=6.2,
            crystal=c_des,
            absorber=absorber_description,
        )
        for c_des in crystal_descriptions
    ]


@pytest.fixture(scope="module")
def templates_path():
    return pathlib.Path.cwd().joinpath("templates")
