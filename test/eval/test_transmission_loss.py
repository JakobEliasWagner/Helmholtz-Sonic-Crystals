import numpy as np
import pytest

from hsc import HelmholtzDataset
from hsc.eval import transmission_loss


@pytest.fixture(scope="module")
def zero_loss_set(example_dataset):
    return HelmholtzDataset(
        frequencies=example_dataset.frequencies,
        x=example_dataset.x,
        p=np.ones(example_dataset.p.shape),
        description=example_dataset.description,
    )


@pytest.fixture(scope="module")
def loss_set(example_dataset):
    return HelmholtzDataset(
        frequencies=example_dataset.frequencies,
        x=example_dataset.x,
        p=np.random.rand(*example_dataset.p.shape),
        description=example_dataset.description,
    )


def test_zero_loss(zero_loss_set):
    assert np.allclose(
        transmission_loss(zero_loss_set, p_0=1.0),
        np.zeros(zero_loss_set.frequencies.shape),
    )
    assert np.allclose(
        transmission_loss(zero_loss_set), np.zeros(zero_loss_set.frequencies.shape)
    )


def test_smaller_zero(loss_set):
    assert all(transmission_loss(loss_set, p_0=1.0) < 0.0)
