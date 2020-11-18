import tifffile
import numpy as np
from skimage.filters import gaussian


def generate_raw(shape, num_frames, bit_depth=8, num_parts=30, background=10, noise=10):

    rng = np.random.default_rng()

    prob = num_parts / (shape[1] ** 2)

    points = rng.binomial(1, prob, size=shape)
    print("detected :", points.sum())
    max_val = 2 ** bit_depth
    bg = rng.binomial(max_val, background / max_val)
    points = gaussian(points, (10, 3, 3), preserve_range=True)
    points = (points / points.max()) * 100 + bg
    counting_noise = (points ** 0.5) * rng.normal(loc=1, scale=1 / noise, size=shape)
    points += counting_noise
    points = points.clip(0, 255)
    return points.astype(f"uint{bit_depth}")
