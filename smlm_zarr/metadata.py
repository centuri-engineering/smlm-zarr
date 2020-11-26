OMERO_METADATA = {
    "rdefs": {
        "defaultT": 0,
        "defaultZ": 0,
        "model": "greyscale",  # "color" or "greyscale"
        "projection": "normal",
    },
    "channels": [
        {
            "color": "000000",
            "active": True,
            "window": {"max": 65535, "end": 65535, "start": 0, "min": 0},
            "emissionWave": 647,
            "label": "",
        },
    ],
    "meta": {
        "projectDescription": "",
        "datasetName": "",
        "projectId": 0,
        "imageDescription": "",
        "imageTimestamp": 0,
        "imageId": 0,
        "imageAuthor": "",
        "imageName": "",
        "datasetDescription": "",
        "projectName": "",
        "datasetId": 0,
    },
    "id": 0,
    "pixel_size": {"y": 0.107, "x": 0.107, "z": 0.2},
    "size": {"width": 512, "c": 1, "z": 1, "t": 4086, "height": 512},
    "tiles": False,
}

OMERO_METADATA_TILES = OMERO_METADATA.copy()

OMERO_METADATA_TILES.update(
    {
        "tiles": False,
        "tile_size": {"width": 256, "height": 256},
        "levels": 5,
        "zoomLevelScaling": {0: 1, 1: 0.25, 2: 0.0625, 3: 0.0312, 4: 0.0150},
    }
)


def get_omero_metadata(metadata=None, tiles=False):
    """Returns an omero metadata dict with default values
    """
    if tiles:
        metadata_ = OMERO_METADATA_TILES.copy()
    else:
        metadata_ = OMERO_METADATA.copy()

    if metadata is not None:
        metadata_.update(metadata)

    return metadata_


TABLE_METADATA = {
    "colmuns": ["id", "x", "y", "z", "t", "I", "sigma_x", "sigma_y", "sigma_z"],
}


def get_table_metadata(metadata=None):
    """Returns
    """
    metadata_ = TABLE_METADATA.copy()
    if metadata is not None:
        metadata_.update(metadata)
    return metadata_
