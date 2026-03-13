# ---- This is <utils.py> ----

"""
Utils for handling search and download results from CDSE.
"""

import sys
import pathlib
import os

from dotenv import load_dotenv

from loguru import logger

from shapely.wkt import loads
from shapely.geometry import Polygon
import json

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_product_names_from_response_json(response_json):
    """
    Extract list of product names from CDSE response in json format (dict)

    Parameters
    ----------
    response_json : CDSE response in json format (dict)

    Returns
    -------
    product_names : list of product names
    """    

    # initalize empty list
    product_names = []

    # get product_list from response_json
    product_list = response_json['value']

    for product in product_list:
        logger.debug(f"Appending current product name: {product['Name']}")
        product_names.append(product['Name'])

    return product_names

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_user_and_passwd(dotenv_path='.env'):
    """
    Read CDSE username and password from hidden .env file

    Parameters
    ----------
    dotenv_path : path to hidden .env file

    Returns
    -------
    CDSE_user : CDSE user name
    CDSE_passwd : CDSE password
    """    

    logger.debug('Loading environment variables from .env file')

    CDSE_user = []
    CDSE_passwd = []

    dotenv_path = pathlib.Path(dotenv_path).resolve()

    if not dotenv_path.is_file():
        logger.error(f"Could not find 'dotenv_path': {dotenv_path}")
        return CDSE_user, CDSE_passwd

    load_dotenv(dotenv_path)

    try:
        CDSE_user = os.environ["CDSE_USER"]
    except:
        logger.error("The environment variable 'CDSE_USER' is not set.")
        return CDSE_user, CDSE_passwd

    try:
        CDSE_passwd = os.environ["CDSE_PASSWORD"]
    except:
        logger.error("The environment variable 'CDSE_PASSWORD' is not set.")
        return CDSE_user, CDSE_passwd


    return CDSE_user, CDSE_passwd

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_product_footprint_and_center(p):
    """
    Extract footprint and center from input product dict

    Parameters
    ----------
    p : single product dict

    Returns
    -------
    polygon : shapely.geometry.polygon.Polygon of product footprint
    center : lat/lon of footprint central point as list ([lat, lon])
    """

    logger.debug("Extracting product footprint and central lat/lon")

    # Initialize empty returns
    footprint = center = []

    if not type(p)==dict:
        logger.error(f"Expected input type dict, but received type: {type(p)}")
        return footprint, center

    if not "Footprint" in p.keys():
        logger.error(f"Product does not contain footprint information.")
        return footprint, center

    # Get footprint of example product
    footprint = p["Footprint"].split(";")[1]

    # Load the polygon using shapely
    polygon = loads(footprint)

    logger.debug(f"Read product's footprint polygon: {polygon}")

    # Get the centroid of the polygon
    centroid = polygon.centroid

    logger.debug(f"Extracted polygon centroid: {centroid}")

    # Extract the coordinates of the centroid
    center = [centroid.y, centroid.x]

    return polygon, center

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def write_polygon_2_geojson(polygon, geojson_path):
    """
    Export a shapely.geometry.polygon.Polygon as geojson file.

    Parameters
    ----------
    polygon : shapely.geometry.polygon.Polygon of product footprint
    geojson_path : path to output geojson file

    Returns
    -------
    geojson : True/False
    """

    logger.debug("Exporting shapely.geometry.polygon.Polygon as geojson file")

    if not isinstance(polygon, Polygon):
        logger.error(f"Expected input type shapely.geometry.polygon.Polygon, but received type: {type(polygon)}")
        return False

    # Convert to GeoJSON format
    geojson_str = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": json.loads(json.dumps(polygon.__geo_interface__)),  # Use shapely's GeoJSON interface
                "properties": {}
            }
        ]
    }

    # Save the GeoJSON to a file
    with open(geojson_path, "w") as f:
        json.dump(geojson_str, f, indent=4)
    logger.debug(f"GeoJSON file saved as {geojson_path}")

    return True

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <utils.py> ----
