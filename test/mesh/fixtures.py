import pathlib

import pytest

from hsc.domain_properties import (
    CShapeDescription,
    CylinderDescription,
    NoneDescription,
    read_config,
)


@pytest.fixture(scope="module")
def template_descriptions():
    templates = pathlib.Path.cwd().joinpath("templates")
    files = templates.glob("*.ini")
    descriptions = []
    for file in files:
        descriptions.extend(read_config(file))
    return descriptions


@pytest.fixture(scope="module")
def template_cylindrical_descriptions(template_descriptions):
    return [
        des
        for des in template_descriptions
        if isinstance(des.crystal, CylinderDescription)
    ]


@pytest.fixture(scope="module")
def template_c_shaped_descriptions(template_descriptions):
    return [
        des
        for des in template_descriptions
        if isinstance(des.crystal, CShapeDescription)
    ]


@pytest.fixture(scope="module")
def template_none_descriptions(template_descriptions):
    return [
        des for des in template_descriptions if isinstance(des.crystal, NoneDescription)
    ]
