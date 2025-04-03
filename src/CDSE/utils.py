# ---- This is <utils.py> ----

"""
Utils for handling search and download results from CDSE.
"""

import sys
import pathlib

from loguru import logger

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_product_names_from_response_json(response_json, loglevel='INFO'):
    """
    Extract list of product names from CDSE response in json format (dict)

    Parameters
    ----------
    response_json : CDSE response in json format (dict)
    loglevel : loglevel setting (default='INFO')

    Returns
    -------
    product_names : list of product names
    """    

    # remove default logger handler and add personal one
    logger.remove()
    logger.add(sys.stderr, level=loglevel)

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

# ---- End of <utils.py> ----
