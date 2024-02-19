import pathlib

import pytest

from hsc import HelmholtzDataset


@pytest.fixture(scope="session")
def example_dset_dir():
    return pathlib.Path().cwd().joinpath("data", "example_dset")


@pytest.fixture(scope="session")
def example_xdmf(example_dset_dir) -> pathlib.Path:
    return next(example_dset_dir.glob("*.xdmf"))


@pytest.fixture(scope="session")
def example_dataset(example_xdmf) -> HelmholtzDataset:
    return HelmholtzDataset.from_xdmf_file(example_xdmf)
