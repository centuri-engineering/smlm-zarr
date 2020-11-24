"""Write a variant of OME-ZARR for SMLM data

"""
import subprocess

import numpy as np
import zarr
import tifffile

from .metadata import get_omero_metadata, get_table_metadata


def write_smlm_zarr(
    zarr_directory,
    raw_tiffs=None,
    raw_metadata=None,
    localizations=None,
    loc_metadata=None,
    rendered=None,
    rendered_metadata=None,
):
    metadata = get_omero_metadata(raw_metadata)
    store = zarr.DirectoryStore(zarr_directory)
    root = zarr.group(store)
    root.attrs["omero"] = metadata
    if raw_tiffs is not None:
        raw = root.create_group("raw")
        # TODO multithread this
        for offset, tiff_stack in enumerate(raw_tiffs):
            # TODO metadata for each sub-tiff ?
            write_2d_tiff(tiff, grp)

    if localizations is not None:
        loc = root.create_group("loc")
        loc.attrs["table"] = get_table_metadata(loc_metadata)
        loc_data = np.loadtxt(localizations)
        loc.create_dataset(0, data=loc_data)

    if rendered is not None:
        rdr = root.create_group("rendered")
        rdr.attrs["omero"] = get_omero_metadata(rendered_metadata)
        write_2d_tiff(rendered, rdr)


def write_2d_tiff(tiff, group):

    ## https://forum.image.sc/t/software-recommendations-converting-a-32bit-ome-tiff-to-an-8bit-ome-tiff/43043/15
    with tifffile.imread(tiff, aszarr=True) as in_store:
        with zarr.open(in_store, mode="r") as in_group:
            zarr.copy(in_group, group)
