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
