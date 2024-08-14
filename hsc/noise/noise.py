from abc import ABC, abstractmethod

import numpy as np


class Noise(ABC):
    @abstractmethod
    def sample(self, src: np.ndarray, tile: str = "") -> np.ndarray:
        pass

    def __call__(self, src: np.ndarray, tile: str = "") -> np.ndarray:
        return self.sample(src=src, tile=tile)
