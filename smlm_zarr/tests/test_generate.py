import numpy as np
from smlm_zarr import generate


def test_generate_single():
    im1 = generate.raw(
        shape=(256, 256),
        bit_depth=16,
        num_parts=30,
        background=30,
        noise=10,
        gaussian_blur=3,
        return_locs=False,
    )
    assert im1.shape == (256, 256)
    assert im1.dtype == np.uint16
    assert im1.max() > 0


def test_generate_single_with_locs():

    im1, locs = generate.raw(
        shape=(256, 256, 13),
        bit_depth=8,
        num_parts=30,
        background=30,
        noise=10,
        gaussian_blur=3,
        return_locs=True,
    )
    assert im1.shape == (256, 256, 13)
    assert im1.dtype == np.uint8
    assert locs.shape[1] == 5
    assert locs.shape[0] > 0


def test_generate_iter():
    iterable = generate.iterable_raw(num_t=6, shape=(10, 10), return_locs=False)
    assert hasattr(iterable, "__iter__")
    for t, im in enumerate(iterable):
        assert im.shape == (10, 10)
    assert t == 5
