import os
import time
from typing import List

import numpy as np
from scipy.signal import convolve2d

from .noise import Noise
from .perlin import Perlin


class LimitedPerlin(Noise):
    def __init__(self, n: List[int], smoothing_steps: int = 1):
        self.noises = [Perlin(n=ni) for ni in n]

        self.smoothing_kernel = (
            1
            / 273
            * np.array(
                [
                    [1, 4, 7, 4, 1],
                    [4, 16, 26, 16, 4],
                    [7, 26, 41, 26, 7],
                    [4, 16, 26, 16, 4],
                    [1, 4, 7, 4, 1],
                ]
            )
        )
        self.smoothing_steps = smoothing_steps

    def sample(self, src: np.ndarray, tile: str = "") -> np.ndarray:
        np.random.seed(
            (os.getpid() * int(time.time())) * np.random.randint(0, 2**32) % 123456789
        )  # for multiprocessing
        f = np.mean(np.stack([noise(src) for noise in self.noises], axis=-1), axis=-1)

        n_grid = int(f.size**0.5)
        assert n_grid**2 == f.size, "grid needs to be square"

        f = f.reshape(n_grid, n_grid)

        for _ in range(self.smoothing_steps):
            f = convolve2d(f, self.smoothing_kernel, boundary="symm", mode="same")

        # cone to limit the crystal to the center
        g = 1 - 2 * src[:, 0] ** 2 - 2 * src[:, 1] ** 2
        g[g < 0] = 0

        g = g.reshape(n_grid, n_grid)
        f = f * g

        return f
