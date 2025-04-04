# ---- This is <json_utils.py> ----

"""
json and geojson utils for search and download from CDSE.
"""

import sys
import pathlib

from loguru import logger

import json
import geojson
import geomet.wkt
import re

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def write_response_dict_2_json(response_dict, output_file):
    """
    Write dictionary to json file

    Parameters
    ----------
    response_dict : dictionary with CDSE response
    output_file : output json json file
    """    

    if type(response_dict) is not dict:
        logger.error(f"Expected input type 'dict' but received {type(response_dict)}")
        return

    if not output_file.endswith('json'):
        logger.error("Output should be a json (or geojson) file")
        return

    with open(output_file, 'w') as fout:
        json.dump(response_dict , fout)

    return




def read_response_dict_from_json(json_path):
    """
    Load a json file into a dictionary

    Parameters
    ----------
    json_path : path to json file

    Returns
    -------
    json_obj : dictionary with json data
    """

    json_path  = pathlib.Path(json_path).resolve()

    if not json_path.exists():
        logger.error(f'Cannot find json_path: {json_path}')
        json_obj = []
        return json_obj

    with open(json_path) as f:
        json_obj = json.load(f) 

    return json_obj

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def read_geojson(geojson_path):
    """
    Load a GeoJSON file into geojson object

    Parameters
    ----------
    geojson_path : path to geojson file

    Returns
    -------
    geojson_obj : dictionary with geojson data
    """

    geojson_path  = pathlib.Path(geojson_path).resolve()

    if not geojson_path.exists():
        logger.error(f'Cannot find geojson_path: {geojson_path}')
        geojson_obj = []
        return geojson_obj

    with open(geojson_path) as f:
        geojson_obj = geojson.load(f) 

    return geojson_obj

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def convert_geojson_obj_2_wkt(geojson_obj, decimals=4):
    """
    Convert a GeoJSON object to well-known text.
    Intended for use with OpenSearch queries.
    3D points are converted to 2D.

    Parameters
    ----------
    geojson_obj : dictionary with geojson data
    decimals : number of decimal to round coordinate to (default=4)

    Returns
    -------
    aoi_string : well-known text string representation of the geometry
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

def get_aoi_string_from_geojson(geojson_path, decimals=4):
    """
    Convert content of a GeoJSON file to well-known text.
    Intended for use with OpenSearch queries.
    3D points are converted to 2D.

    Parameters
    ----------
    geojson_path : path to geojson file
    decimals : number of decimal to round coordinate to (default=4)

    Returns
    -------
    aoi_string : Well-Known Text string representation of the geometry
    """

    geojson_obj = read_geojson(geojson_path)

    aoi_string = convert_geojson_obj_2_wkt(geojson_obj, decimals=decimals)

    return aoi_string

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_aoi_string_from_lat_lon_dict(lat_lon_dict, decimals=4):
    """
    Convert lat/lon keys from dictionary to well-known text.
    Intended for use with OpenSearch queries.

    Parameters
    ----------
    lat_lon_dict : input dictionary with 'lat' and 'lon' keys
    decimals : number of decimal to round coordinate to (default=4)

    Returns
    -------
    aoi_string : Well-Known Text string representation of the geometry
    """

    if type(lat_lon_dict) is not dict:
        logger.error(f"Expected input of type 'dict', but received type '{type(lat_lon_dict)}'")
        ##return aoi_string
 
    if not 'lat' in lat_lon_dict.keys() or not 'lon' in lat_lon_dict.keys():
       logger.error(f"Input dictionary must contain 'lat' and 'lon' keys")
       ##return aoi_string

    # combine lat lon to dictionary of type geojson feature (type: 'POINT')
    D = dict()
    D['type'] = 'Point'
    D['coordinates'] = [lat_lon_dict['lon'], lat_lon_dict['lat']]

    aoi_string = convert_geojson_obj_2_wkt(D, decimals=decimals)

    logger.debug(f"aoi_string: {aoi_string}")

    return aoi_string

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <json_utils.py> ----
