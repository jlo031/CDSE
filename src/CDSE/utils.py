# ---- This is <utils.py> ----

"""
Utils for handling search and download results from CDSE.
"""

import sys
import pathlib
import os

from dotenv import load_dotenv

from loguru import logger

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



# ---- End of <utils.py> ----
