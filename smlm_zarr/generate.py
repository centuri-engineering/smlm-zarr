import tifffile
import numpy as np
from skimage.filters import gaussian


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
    image : np.ndarray of shape `shape`
       The generated image
    locs : np.ndarray of shape (N, len(shape))
       The praticle positions in image coordinates
       (only if return_locs is True)


    Note
    ----
    This is not sophisticated enough to evaluate detection algorithms
    """
    rng = np.random.default_rng()
    prob = num_parts / (shape[1] ** 2)
    max_val = 2 ** bit_depth
    points = rng.binomial(1, prob, size=shape)
    print("detected :", points.sum())
    if return_locs:
        locs = np.array(np.nonzero(points)).T
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
    for i in range(num_t):
        yield raw(*args, **kwargs)


def stacked_raw(num_t, *args, **kwargs):
    if kwargs.get("return_locs"):
        imgs = []
        locs = []
        for i, (img, loc) in enumerate(iterable_raw(num_t, *args, **kwargs)):
            imgs.append(img)
            loc = np.hstack([loc, np.ones((loc.shape[0], 1)) * i])
            locs.append(loc)

        return np.stack(imgs), np.concatenate(locs)
    return np.stack(list(iterable_raw(num_t)))
