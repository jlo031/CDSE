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

import CDSE.json_utils as CDSE_json
import CDSE.access_token_credentials as CDSE_atc

from loguru import logger

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def search_CDSE_catalogue(
    sensor,
    area,
    start_date,
    end_date,
    start_time = None,
    end_time = None,
    max_results = 100,
    max_cloud_cover = None,
    sensor_mode = None,
    processing_level = None,
    expand_attributes = True
):
    """
    Search the CDSE data catalogue for satelite products.

    Parameters
    ----------
    sensor : sensor collection to search (SENTINEL-1, SENTINEL-2)
    area : geojson file with search area
    start_date : start date, format YYYY-MM-DD
    end_date : end date, format YYYY-MM-DD
    start_time : start time, format hh:mm:ss (default=00:00:00)
    end_time : end time, format hh:mm:ss (default=00:00:00)
    max_results : maximum number of items returned from a query
    max_cloud_cover : maximum cloud cover (default=None)
    sensor_mode : sensor mode (default=None)
    processing_level : data processing level (default=None)
   expand_Attributes : see the full metadata of each returned result (default=True)

    Returns
    -------
    response_json : CDSE response in json format (dict)
    """

    # ------------------------ #

    # define valid parameter choices
    valid_sensors = ['SENTINEL-1', 'Sentinel-1', 'SENTINEL-2', 'Sentinel-2']
    valid_modes = ['EW', 'IW']
    datestring_length = 10
    datesplit_length = 3
    timetring_length = 8
    timesplit_length = 3
    valid_levels = [0,1]

    # initialize empty response
    response_json = None

    # ------------------------ #

    # check user inputs

    # sensor
    if sensor not in valid_sensors:
        logger.info(f"Implemented sensors are: {valid_sensors}")
        logger.error(f"Sensor '{sensor}' is not a valid sensor")
        return

    # area
    geojson_path  = pathlib.Path(area).resolve()
    if not geojson_path.exists():
        logger.error(f"Cannot find search area file: '{geojson_path}'")
        return

    # start_date and end_date
    for test_date in [start_date, end_date]:
        logger.debug(f"Checking date input: '{test_date}'")
        if len(test_date) is not datestring_length or len(test_date.split('-')) is not datesplit_length:
            logger.info("Date format must be: 'YYYY-MM-DD'")
            logger.error(f"Input date '{test_date}' is not a correct date format")
            return

    # start_time and end_time
    for test_time in [start_time, end_time]:
        if test_time is not None:
            logger.debug(f"Checking date input: '{test_time}'")
            if len(test_time) is not timetring_length or len(test_time.split(':')) is not timesplit_length:
                logger.info("Time format must be: 'hh:mm:ss'")
                logger.error(f"Input time '{test_time}' is not a correct test_time format")
                return

    # max_results
    if max_results<1 or max_results>1000:
        logger.error(f"max_results: '{max_results}' is outside valid range [1,1000]")
        return

    # max_cloud_cover
    if max_cloud_cover is not None:
        logger.debug("Checking 'max_cloud_cover' input")
        if max_cloud_cover<0 or max_cloud_cover>100:
            logger.error(f"max_cloud_cover: '{max_cloud_cover}' is outside valid range [0,100]")
            return

    # sensor_mode
    if sensor_mode is not None:
        logger.debug("Checking 'sensor_mode' input")
        if sensor_mode not in valid_modes:
            logger.info(f"Implemented sensor modes are: {valid_modes}")
            logger.error(f"'{sensor_mode}' is not a valid sensor mode")
            return

    # processing_level
    if processing_level is not None:
        logger.debug("Checking 'processing_level' input")
        if processing_level not in valid_levels:
            logger.info(f"Implemented processing levels are: {valid_levels}")
            logger.error(f"'{processing_level}' is not a valid processing level")
            return

    # ------------------------ #

    # read aoi string
    aoi = CDSE_json.get_aoi_string_from_geojson(geojson_path, decimals=3)

    # ------------------------ #

    # build the query url

    # build query string: sensor
    querySTR_sensor = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{sensor}'"
    logger.debug(f"querySTR_sensor: {querySTR_sensor}")

    # build query string: area
    querySTR_area =  " and " + f"OData.CSC.Intersects(area=geography'SRID=4326;{aoi}')"
    logger.debug(f"querySTR_area: {querySTR_area}")

    # build query string: time
    if start_time == None and end_time == None:
        querySTR_time = " and " + f"ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T00:00:00.000Z"
    else:
        querySTR_time = " and " + f"ContentDate/Start gt {start_date}T{start_time}.000Z and ContentDate/Start lt {end_date}T{end_time}.000Z"
    logger.debug(f"querySTR_time: {querySTR_time}")

    # build query string: max cloud cover
    if sensor == 'SENTINEL-2' and max_cloud_cover is not None:
        querySTR_max_cloud = " and " + f"Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value le {max_cloud_cover})"
    else:
        querySTR_max_cloud = ""
    logger.debug(f"querySTR_max_cloud: {querySTR_max_cloud}")

    # build query string: mode
    if sensor == 'SENTINEL-1' and sensor_mode is not None:
        querySTR_mode = " and " + f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'operationalMode' and att/OData.CSC.StringAttribute/Value eq '{sensor_mode}')"
    else:
        querySTR_mode = ""
    logger.debug(f"querySTR_mode: {querySTR_mode}")

    # build query string: level
    if sensor == 'SENTINEL-1' and processing_level is not None:
        querySTR_level = " and " + f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'processingLevel' and att/OData.CSC.StringAttribute/Value eq 'LEVEL{processing_level}')"
    else:
        querySTR_level = ""
    logger.debug(f"querySTR_level: {querySTR_level}")

    if expand_attributes:
        querySTR_expand_attributes = "&$expand=Attributes"
    else:
        querySTR_expand_attributes = ""


    # build query string: max_results
    #querySTR_max_results = f"&$top={max_results}"
    #logger.debug(f"querySTR_time: {querySTR_time}")

    # ------------------------ #

    # build full query string
    querySTR = f"{querySTR_sensor}{querySTR_area}{querySTR_max_cloud}{querySTR_mode}{querySTR_level}{querySTR_time}{querySTR_expand_attributes}"

    logger.info(f"Full query string: {querySTR}")

    # ------------------------ #

    # search the data collection
    response_json = requests.get(querySTR).json()
    #product_list = response_json['value']


    return response_json

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
