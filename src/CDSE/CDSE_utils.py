# ---- This is <CDSE_utils.py> ----

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
    R : Feature collection from geojson file
    """

    geojson_path  = pathlib.Path(geojson_path).resolve()

    if not geojson_path.exists():
        logger.error(f'Cannot find geojson_path: {geojson_path}')
        R = []
        return R

    with open(geojson_path) as f:
        R = geojson.load(f) 

    if not 'features' in R.keys():
        logger.error(f'Geojson file does not contain features')
        return R

    return R















def geojson_to_wkt(geojson_obj, decimals=4):
    """Convert a GeoJSON object to Well-Known Text. Intended for use with OpenSearch queries.
    3D points are converted to 2D.

    Parameters
    ----------
    geojson_obj : dict
        a GeoJSON object
    decimals : int, optional
        Number of decimal figures after point to round coordinate to. Defaults to 4 (about 10
        meters).

    Returns
    -------
    str
        Well-Known Text string representation of the geometry
    """
    if "coordinates" in geojson_obj:
        geometry = geojson_obj
    elif "geometry" in geojson_obj:
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




















def write_product_list_to_json_file(product_list, output_file):
    """
    Write product list to json file

    Parameters
    ----------
    product_list : list of products
    output_file : output json json file
    """    

    with open(output_file, 'w') as fout:
        json.dump(product_list , fout)

    return



def write_product_namestrings_to_txt_file(product_list, output_file):
    """
    Write product list to json file

    Parameters
    ----------
    product_list : list of products
    output_file : output txt json file
    """    

    product_names = []

    for product in product_list:
        product_names.append(product['Name'])

    with open(output_file, "w") as fout:
        fout.write("\n".join(product_names))
    
    return



# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <CDSE_utils.py> ----
