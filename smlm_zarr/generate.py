"""Utility function to generate smlm looking raw images

"""
import logging

import numpy as np
from skimage.filters import gaussian


log = logging.getLogger(__name__)


def raw(
    shape=(512, 512),
    bit_depth=8,
    num_parts=30,
    background=50,
    noise=10,
    gaussian_blur=3,
    return_locs=False,
):
    """Generate a numpy array with spots resembling single molecule data

    Parameters
    ----------
    shape: tuple of ints
       the shape of the image
    bit_depth: int
       bit depth of the image (8, 16, 32 or 64)
    num_parts: int
       approximate number of particles detected in the image
    backround: int
       typical background intensity
    noise: float
       counting noise (as % of sqrt(I))
    gaussian_blur: float
       width of the blur
    return_locs: bool
       Whether to also return spots localization

    Returns
    -------
    image : np.ndarray of shape `(shape, shape)`
       The generated image
    locs : np.ndarray of shape (N, 5)
       The praticle positions in image coordinates
       (only if return_locs is True)
       images coordinates are 5D by default with order
       "x", "y", "z", "c", "t"


    Note
    ----
    This is not sophisticated enough to evaluate detection algorithms
    """
    rng = np.random.default_rng()
    prob = num_parts / (shape[1] ** 2)
    max_val = 2 ** bit_depth
    points = rng.binomial(1, prob, size=shape)
    log.info("detected : %d", points.sum())
    if return_locs:
        coords = np.nonzero(points)
        # xyzct
        locs = np.zeros((coords[0].shape[0], 5), dtype="uint64")
        for i, cc in enumerate(coords):
            locs[:, i] = cc

    points *= rng.normal(max_val / 2, max_val / 10, size=shape).astype(np.int64)
    bg = rng.binomial(max_val, background / max_val, size=shape)

    image = (
        gaussian(points, gaussian_blur, preserve_range=True) * (gaussian_blur ** 2) + bg
    )

    counting_noise = (image ** 0.5) * rng.normal(loc=1, scale=1 / noise, size=shape)
    image += counting_noise
    image = image.clip(0, 2 ** bit_depth).astype(f"uint{bit_depth}")
    if return_locs:
        # Guess what?
        return image, locs
    return image


def iterable_raw(num_t, *args, **kwargs):
    """Generate an iterator yielding raw planes

    See Also
    --------
    raw : gets the args and kwargs
    """
    for t in range(num_t):
        if kwargs.get("return_locs"):
            img, locs = raw(*args, **kwargs)
            locs[:, -1] = t
            yield img, locs
        else:
            yield raw(*args, **kwargs)


def stacked_raw(num_t, *args, **kwargs):
    if kwargs.get("return_locs"):
        imgs = []
        locs = []
        for img, loc in iterable_raw(num_t, *args, **kwargs):
            imgs.append(img)
            locs.append(loc)

        return np.stack(imgs), np.concatenate(locs).astype("uint64")
    return np.stack(list(iterable_raw(num_t)))
