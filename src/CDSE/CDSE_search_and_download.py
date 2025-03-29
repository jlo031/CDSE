# ---- This is <CDSE_search_and_download.py> ----

"""
Utils for search and download from CDSE.
"""

import pathlib
import json
import geojson
import geomet.wkt
import re

import requests

from loguru import logger

import CDSE.access_token_credentials as CDSE_atc
import CDSE.CDSE_utils as CDSE_utils
import CDSE.geojson_utils as CDSE_geo

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def search_CDSE_catalogue(
    sensor,
    area,
    start_date,
    end_date,
    max_cloud_cover = None
):
    """
    Search the CDSE data catalogue for satelite products.

    Parameters
    ----------
    sensor : sensor collection to search (SENTINEL-1, SENTINEL-2)
    area : geojson file with search area
    start_date : start date, format YYYY-MM-DD
    end_date : end date, format YYYY-MM-DD
    max_cloud_cover : maximum cloud cover (default=None)

    Returns
    -------
    D : Dictionary with geojson data
    """

    # check user inputs

    sensor_list = ['SENTINEL-1', 'Sentinel-1', 'SENTINEL-2', 'Sentinel-2']

    if sensor not in sensor_list:
        logger.info(f"Implemented sensors are: {sensor_list}")
        logger.error(f"{sensor} is not a valid sensor")
        return




    geojson_path  = pathlib.Path(area).resolve()
    if not geojson_path.exists():
        logger.error(f'Cannot find search area file: {geojson_path}')
        return






    with open(geojson_path) as f:
        D = geojson.load(f) 

    if not 'features' in D.keys():
        logger.error(f'Geojson file does not contain features')
        return D

    return D

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

#product = response_dict['value'][3]

def download_product_from_cdse(product, download_dir, username, password, overwrite=False, chunk_size=8192):
    """
    Download zipped product directly from CDSE 

    Parameters
    ----------
    product : product dictionary (returned from request)
    download_dir : download directory
    username : CDSE username
    password : CDSE password
    overwrite : overwrite existing files (default=False)
    chunk_size : download in chunks (default=8192)

    Returns
    -------
    downloaded : True/False for succesful download
    """

    # check product for download
    if type(product) is not dict:
        logger.error(f"Expected product type 'dict' but received {type(product)}")
        return

    logger.info(f"Preparing to download product: {product['Name']}")

    # check download_dir
    download_dir = pathlib.Path(download_dir)
    if not download_dir.is_dir():
        logger.error(f"Could not find download directory {download_dir}")
        return

    # build full download path
    download_zip_path  = download_dir / f"{product['Name'].split('.SAFE')[0]}.zip"
    download_safe_path = download_dir / f"{product['Name']}"

    logger.debug(f"download_zip_path:  {download_zip_path}")
    logger.debug(f"download_safe_path: {download_safe_path}")

    # check for existing products
    if download_zip_path.is_file() or download_safe_path.is_dir() and not overwrite:
        logger.info("Product already exists")
        return


    # build download url for current product
    url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({product['Id']})/$value"

    # generate access token
    access_token = CDSE_atc.get_access_token(username, password)

    headers = {"Authorization": f"Bearer {access_token}"}

    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url, headers=headers, stream=True)

    with open(download_zip_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    session.close()
    response.close()

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def download_product_list_from_cdse(product_list, download_dir, username, password, overwrite=False, chunk_size=8192):
    """
    Download list of zipped product directly from CDSE 

    Parameters
    ----------
    product_list : product lsit with dictionaries for individual products (returned from request)
    download_dir : download directory
    username : CDSE username
    password : CDSE password
    overwrite : overwrite existing files (default=False)
    chunk_size : download in chunks (default=8192)

    Returns
    -------
    downloaded : True/False for succesful download
    """

    # check product_list for download
    if type(product_list) is not list:
        logger.error(f"Expected product_list type 'list' but received {type(product)}")
        return

    # get number of entries
    n_products =len(product_list)

    logger.info(f"Preparing download of {n_products} products in product_list")

    for i,product in enumerate(product_list):
        logger.info(f"Downloading product {i+1} of {n_products}")

        download_product_from_cdse(
            product,
            download_dir,
            username,
            password,
            overwrite=overwrite,
            chunk_size=chunk_size)


    return

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <CDSE_search_and_download.py> ----
