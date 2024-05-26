from typing import Callable

import numpy as np

from .noise import Noise


def smooth_step(src: np.ndarray) -> np.ndarray:
    return src**2 * (3 - 2 * src)


def fifth_order_smoothing(src: np.ndarray) -> np.ndarray:
    return src**3 * (6 * src**2 - 15 * src + 10)


class Perlin(Noise):
    def __init__(
        self,
        n: int = 7,
        smoothing_function: Callable = fifth_order_smoothing,
        epsilon: float = 1e-6,
    ):
        self.h = smoothing_function
        self.n = n

        self.border_xx = np.linspace(0, 1, n)
        self.border_yy = np.linspace(0, 1, n)

        self.epsilon = epsilon

    def sample(self, src: np.ndarray, tile: str = "") -> np.ndarray:
        assert src.ndim == 2
        assert src.shape[-1] == 2

        # scale src to [0, 1)
        src_min = np.min(src, axis=0, keepdims=True)
        src_max = np.max(src, axis=0, keepdims=True)
        src = (src - src_min) / (src_max - src_min) * (1 - self.epsilon)

        if "x" in tile:
            src[:, 0] = np.sin(src[:, 0] * np.pi)
        if "y" in tile:
            src[:, 1] = np.sin(src[:, 1] * np.pi)

        # randomly sample gradients
        gradients = np.random.rand(self.n, self.n, 2) - 0.5

        # scale to unit length
        gradients = gradients / np.sqrt(
            np.sum(gradients.reshape(-1, 2) ** 2, axis=1)
        ).reshape(self.n, self.n, 1)

        # index array
        xx_idx = np.searchsorted(self.border_xx, src[:, 0], side="right") - 1
        yy_idx = np.searchsorted(self.border_yy, src[:, 1], side="right") - 1

        # distance
        dist_x = (src[:, 0] - self.border_xx[xx_idx]) / (
            self.border_xx[xx_idx + 1] - self.border_xx[xx_idx]
        )
        dist_y = (src[:, 1] - self.border_yy[yy_idx]) / (
            self.border_yy[yy_idx + 1] - self.border_yy[yy_idx]
        )

        # s upper left
        s_ul = gradients[xx_idx, yy_idx, 0] * (
            src[:, 0] - self.border_xx[xx_idx]
        ) + gradients[xx_idx, yy_idx, 1] * (src[:, 1] - self.border_yy[yy_idx])

        # s upper right
        s_ur = gradients[xx_idx + 1, yy_idx, 0] * (
            src[:, 0] - self.border_xx[xx_idx + 1]
        ) + gradients[xx_idx + 1, yy_idx, 1] * (src[:, 1] - self.border_yy[yy_idx])

        # s lower left
        s_ll = gradients[xx_idx, yy_idx + 1, 0] * (
            src[:, 0] - self.border_xx[xx_idx]
        ) + gradients[xx_idx, yy_idx + 1, 1] * (src[:, 1] - self.border_yy[yy_idx + 1])

        # s lower right
        s_lr = gradients[xx_idx + 1, yy_idx + 1, 0] * (
            src[:, 0] - self.border_xx[xx_idx + 1]
        ) + gradients[xx_idx + 1, yy_idx + 1, 1] * (
            src[:, 1] - self.border_yy[yy_idx + 1]
        )

        # dot product
        f0 = s_ul * self.h(1 - dist_x) + s_ur * self.h(dist_x)
        f1 = s_ll * self.h(1 - dist_x) + s_lr * self.h(dist_x)
        f = f0 * self.h(1 - dist_y) + f1 * self.h(dist_y)

        return f / np.max(np.abs(f))
