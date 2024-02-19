import pathlib

import pytest

from hsc.domain_properties import (CShapeDescription, CylinderDescription,
                                   NoneDescription, read_config)


@pytest.fixture(scope="module")
def descriptions():
    templates = pathlib.Path.cwd().joinpath("templates")
    files = templates.glob("*.ini")
    descriptions = []
    for file in files:
        descriptions.extend(read_config(file))
    return descriptions


@pytest.fixture(scope="module")
def cylindrical_descriptions(descriptions):
    return [des for des in descriptions if isinstance(des.crystal, CylinderDescription)]


@pytest.fixture(scope="module")
def c_shaped_descriptions(descriptions):
    return [des for des in descriptions if isinstance(des.crystal, CShapeDescription)]


@pytest.fixture(scope="module")
def none_descriptions(descriptions):
    return [des for des in descriptions if isinstance(des.crystal, NoneDescription)]
