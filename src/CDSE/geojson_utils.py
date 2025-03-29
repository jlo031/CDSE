# ---- This is <geojson_utils.py> ----

"""
Utils for search and download from CDSE.
"""

import pathlib
import json
import geojson
import geomet.wkt
import re

from loguru import logger

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def read_geojson(geojson_path):
    """
    Read a GeoJSON file into feature collection

    Parameters
    ----------
    geojson_path : path to geojson file

    Returns
    -------
    D : Dictionary with geojson data
    """

    geojson_path  = pathlib.Path(geojson_path).resolve()

    if not geojson_path.exists():
        logger.error(f'Cannot find geojson_path: {geojson_path}')
        D = []
        return D

    with open(geojson_path) as f:
        D = geojson.load(f) 

    if not 'features' in D.keys():
        logger.error(f'Geojson file does not contain features')
        return D

    return D

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def geojson_to_wkt(geojson_obj, decimals=4):
    """
    Convert a GeoJSON object to Well-Known Text.
    Intended for use with OpenSearch queries.
    3D points are converted to 2D.

    Parameters
    ----------
    geojson_dict : geojson data dictionary
    decimals : number of decimal to round coordinate to (default=4)

    Returns
    -------
    aoi_string : Well-Known Text string representation of the geometry
    """


    # check contents of geojson data and read single or multiple geometries
    if "coordinates" in geojson_obj:
        logger.debug(f"geojson data contains coordinates and geometry type directly")
        geometry = geojson_obj
    elif "geometry" in geojson_obj:
        logger.debug(f"geojson data contains geometry dict with coordinates and geometry type")
        geometry = geojson_obj["geometry"]
    else:
        geometry = {"type": "GeometryCollection", "geometries": []}
        for feature in geojson_obj["features"]:
            geometry["geometries"].append(feature["geometry"])

    def ensure_2d(geometry):
        if isinstance(geometry[0], (list, tuple)):
            return list(map(ensure_2d, geometry))
        else:
            return geometry[:2]

    def check_bounds(geometry):
        if isinstance(geometry[0], (list, tuple)):
            return list(map(check_bounds, geometry))
        else:
            if geometry[0] > 180 or geometry[0] < -180:
                raise ValueError("Longitude is out of bounds, check your JSON format or data")
            if geometry[1] > 90 or geometry[1] < -90:
                raise ValueError("Latitude is out of bounds, check your JSON format or data")

    # Discard z-coordinate, if it exists
    if geometry["type"] == "GeometryCollection":
        for idx, geo in enumerate(geometry["geometries"]):
            geometry["geometries"][idx]["coordinates"] = ensure_2d(geo["coordinates"])
            check_bounds(geo["coordinates"])
    else:
        geometry["coordinates"] = ensure_2d(geometry["coordinates"])
        check_bounds(geometry["coordinates"])

    wkt = geomet.wkt.dumps(geometry, decimals=decimals)

    # Strip unnecessary spaces
    wkt = re.sub(r"(?<!\d) ", "", wkt)

    return wkt

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #


















# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <geojson_utils.py> ----
