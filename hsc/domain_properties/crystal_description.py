import dataclasses
from abc import ABC

import numpy as np


@dataclasses.dataclass
class CrystalDescription(ABC):
    """Holds information about a crystal."""

    grid_size: float
    n: int


@dataclasses.dataclass
class CylinderDescription(CrystalDescription):
    """Holds information about a cylindrical crystal."""

    radius: float


@dataclasses.dataclass
class CShapeDescription(CrystalDescription):
    """Holds information about a C-shaped crystal."""

    radius: float
    inner_radius: float
    gap_width: float


@dataclasses.dataclass
class NoneDescription(CrystalDescription):
    """A domain without crystals."""


@dataclasses.dataclass
class PerlinDescription(CrystalDescription):
    """Holds information about a random perlin noise crystal."""

    n_min: int  # lower perlin noise scale (inclusive)
    n_max: int  # upper perlin noise scale (inclusive)
    n_perlin_grid: int = 301
    smoothing_steps: int = 1

    noise_grid: np.array = None
