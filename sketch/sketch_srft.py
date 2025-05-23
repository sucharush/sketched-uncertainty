from sketch.sketch_base import Sketcher
import numpy as np
from scipy.fft import fft, rfft

class SRFTSketcher(Sketcher):
    def __init__(self, p, s=256, rfft=False):
        self.p = p
        self.s = s
        self.rfft = rfft
        self._D = None
        self._subset = None
        self._initialize_srft()

    def _initialize_srft(self):
        self._D = np.sign(np.random.randn(self.p))
        if self.rfft:
            fft_size = self.p // 2 + 1
        else:
            fft_size = self.p
        self._subset = np.sort(np.random.choice(fft_size, self.s, replace=False))

    def apply_sketch(self, x):
        if self._D is None or self._subset is None:
            self._initialize_srft()

        is_vector = (x.ndim == 1)
        if is_vector:
            x = x[:, np.newaxis]  # (p, 1)

        x_d = self._D[:, None] * x

        if self.rfft:
            x_f = rfft(x_d, axis=0, norm="ortho")
        else:
            x_f = fft(x_d, axis=0, norm="ortho")

        x_sub = x_f[self._subset, :]
        x_sketch = np.sqrt(self.p / self.s) * x_sub

        return x_sketch[:, 0] if is_vector else x_sketch
