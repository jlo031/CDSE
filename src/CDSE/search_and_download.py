# ---- This is <search_and_download.py> ----

"""
Ssearch and download products from CDSE.
"""

import sys
import pathlib

from loguru import logger

import requests

import CDSE.json_utils as CDSE_json
import CDSE.access_token_credentials as CDSE_atc

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def check_CDSE_request_parameters(
    sensor,
    area,
    start_date,
    end_date,
    start_time = "00:00:00",
    end_time = "00:00:00",
    max_results = 1000,
    max_cloud_cover = 100,
    sensor_mode = None,
    product_type = None,
    processing_level = None,
    expand_attributes = True,
    loglevel = 'INFO'
):
    """
    Ensure correct formatting of input parameters for CDSE catalogue request.

    Parameters
    ----------
    sensor : sensor collection to search (SENTINEL-1, SENTINEL-2)
    area : geojson file with search area
    start_date : start date, format YYYY-MM-DD
    end_date : end date, format YYYY-MM-DD
    start_time : start time, format hh:mm:ss (default="00:00:00")
    end_time : end time, format hh:mm:ss (default="00:00:00")
    max_results : maximum number of items returned from a query
    max_cloud_cover : maximum cloud cover (default=100)
    sensor_mode : sensor mode (default=None)
    product_type : product type (default=None)
    processing_level : data processing level (default=None)
    expand_attributes : see the full metadata of each returned result (default=True)
    loglevel : loglevel setting (default='INFO')

    Returns
    -------
    valid_parameters : True/False
    """

    # remove default logger handler and add personal one
    logger.remove()
    logger.add(sys.stderr, level=loglevel)

    # define valid parameter choices
    valid_sensors = ['SENTINEL-1', 'Sentinel-1', 'SENTINEL-2', 'Sentinel-2']
    datestring_length = 10
    datesplit_length = 3
    timetring_length = 8
    timesplit_length = 3
    valid_modes = ['EW', 'IW']
    valid_S1_product_types = ['GRD']
    valid_S2_product_types = ['1C','2A']
    valid_S1_levels = [0,1,'0','1']
    valid_S2_levels = ['1C','2A']
 
    # initialize return Boolean
    valid_parameters = False

    # ------------------------ #

    logger.info("Checking CDSE request parameters")

    # sensor
    logger.debug(f"Checking input 'sensor': {sensor}")
    if sensor not in valid_sensors:
        logger.info(f"Implemented sensors are: {valid_sensors}")
        logger.error(f"Sensor '{sensor}' is not a valid sensor")
        return valid_parameters

    # area
    logger.debug(f"Checking input 'area': {area}")
    geojson_path  = pathlib.Path(area).resolve()
    if not geojson_path.exists():
        logger.error(f"Cannot find search area file: '{geojson_path}'")
        return valid_parameters
    if not geojson_path.suffix.endswith('json'):
        logger.error(f"Input 'area' must be a json file, but file ending is '{geojson_path.suffix}'")
        return valid_parameters

    # start_date and end_date
    for test_date in [start_date, end_date]:
        logger.debug(f"Checking input 'date': {test_date}")
        if len(test_date) is not datestring_length or len(test_date.split('-')) is not datesplit_length:
            logger.info("Date format must be: 'YYYY-MM-DD'")
            logger.error(f"Input date '{test_date}' is not a correct date format")
            return valid_parameters

    # start_time and end_time
    for test_time in [start_time, end_time]:
        logger.debug(f"Checking input 'time': {test_time}")
        if len(test_time) is not timetring_length or len(test_time.split(':')) is not timesplit_length:
            logger.info("Time format must be: 'hh:mm:ss'")
            logger.error(f"Input time '{test_time}' is not a correct test_time format")
            return valid_parameters

    # max_results
    logger.debug(f"Checking input 'max_results': {max_results}")
    if type(max_results) is not int:
        logger.error(f"'max_results' must be an integer number")
        return valid_parameters
    if max_results<1 or max_results>1000:
        logger.error(f"max_results: '{max_results}' is outside valid range [1,1000]")
        return valid_parameters

    # max_cloud_cover
    logger.debug(f"Checking input 'max_cloud_cover': {max_cloud_cover}")
    if type(max_cloud_cover) is not int:
        logger.error(f"'max_cloud_cover' must be an integer number")
        return valid_parameters
    if max_cloud_cover<0 or max_cloud_cover>100:
        logger.error(f"max_cloud_cover: '{max_cloud_cover}' is outside valid range [0,100]")
        return valid_parameters

    # sensor_mode
    if sensor_mode is not None:
        logger.debug(f"Checking input 'sensor_mode': {sensor_mode}")
        if sensor_mode not in valid_modes:
            logger.info(f"Implemented sensor modes are: {valid_modes}")
            logger.error(f"'{sensor_mode}' is not a valid sensor mode")
            return valid_parameters

    # product_type
    if product_type is not None:
        logger.debug(f"Checking input 'product_type': {product_type}")
        if sensor.upper()=='SENTINEL-1' and product_type not in valid_S1_product_types:
            logger.info(f"Implemented S1 product types are: {valid_S1_product_types}")
            logger.error(f"'{product_type}' is not a valid product type for S1")
            return valid_parameters
        elif sensor.upper()=='SENTINEL-2' and product_type not in valid_S2_product_types:
            logger.info(f"Implemented S2 product types are: {valid_S2_product_types}")
            logger.error(f"'{product_type}' is not a valid product type for S2")
            return valid_parameters

    # processing_level
    if processing_level is not None:
        logger.debug(f"Checking input 'processing_level': {processing_level}")
        if sensor.upper()=='SENTINEL-1' and processing_level not in valid_S1_levels:
            logger.info(f"Implemented S1 processing levels are: {valid_S1_levels}")
            logger.error(f"'{processing_level}' is not a valid processing level for S1")
            return valid_parameters
        elif sensor.upper()=='SENTINEL-2' and processing_level not in valid_S2_levels:
            logger.info(f"Implemented S2 processing levels are: {valid_S2_levels}")
            logger.error(f"'{processing_level}' is not a valid processing level for S2")
            return valid_parameters

    # expand_attributes
    logger.debug(f"Checking input 'expand_attributes': {expand_attributes}")
    if type(expand_attributes) is not bool:
        logger.info(f"'expand_attributes' must be boolean expression")
        logger.error(f"'{expand_attributes}' is not a valid expand_attributes")
        return valid_parameters

    if sensor.upper()=='SENTINEL-2' and processing_level is not None and product_type is not None and processing_level is not product_type:
        logger.error(f"'processing_level' and 'product_type' are redundant for S2 and must be the same (or one not set)")
        return valid_parameters

    # ------------------------ #

    logger.info(f"Checked all input parameters")
    valid_parameters = True

    return valid_parameters

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def search_CDSE_catalogue_by_name(product_name, loglevel = 'INFO'):
    """
    Search the CDSE data catalogue specific data product by its exact name.

    Parameters
    ----------
    product_name : exact product name (e.g. S1_EW_GRDM_....)
    loglevel : loglevel setting (default='INFO')

    Returns
    -------
    response_json : CDSE response in json format (dict)
    """

    # sensor
    querySTR = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Name eq 'S1A_IW_GRDH_1SDV_20141031T161924_20141031T161949_003076_003856_634E.SAFE'"
    logger.debug(f"querySTR: {querySTR}")


    # search the data collection
    response_json = requests.get(querySTR).json()

    # extract list of products 
    product_list = response_json['value']

    logger.info(f"Query found {len(product_list)} products")

    return response_json








def search_CDSE_catalogue(
    sensor,
    area,
    start_date,
    end_date,
    start_time = "00:00:00",
    end_time = "00:00:00",
    max_results = 1000,
    max_cloud_cover = 100,
    sensor_mode = None,
    product_type = None,
    processing_level = None,
    expand_attributes = True,
    loglevel = 'INFO'
):
    """
    Search the CDSE data catalogue for satelite products.

    Parameters
    ----------
    sensor : sensor collection to search (SENTINEL-1, SENTINEL-2)
    area : geojson file with search area
    start_date : start date, format YYYY-MM-DD
    end_date : end date, format YYYY-MM-DD
    start_time : start time, format hh:mm:ss (default="00:00:00")
    end_time : end time, format hh:mm:ss (default="00:00:00")
    max_results : maximum number of items returned from a query
    max_cloud_cover : maximum cloud cover (default=100)
    sensor_mode : sensor mode (default=None)
    product_type : product type (default=None)
    processing_level : data processing level (default=None)
    expand_attributes : see the full metadata of each returned result (default=True)
    loglevel : loglevel setting (default='INFO')

    Returns
    -------
    response_json : CDSE response in json format (dict)
    """

    # remove default logger handler and add personal one
    logger.remove()
    logger.add(sys.stderr, level=loglevel)

    # initialize empty response_json
    response_json = []

    # ------------------------ #

    # check input parameters
    valid_input = check_CDSE_request_parameters(
        sensor = sensor,
        area = area,
        start_date = start_date,
        end_date = end_date,
        start_time = start_time,
        end_time = end_time,
        max_results = max_results,
        max_cloud_cover = max_cloud_cover,
        sensor_mode = sensor_mode,
        product_type = product_type,
        processing_level = processing_level,
        expand_attributes = expand_attributes,
        loglevel = loglevel
    )

    if not valid_input:
        logger.error(f"Invalid search parameters")
        return response_json

# -------------------------------------------------------------------------- #

    # read aoi string
    aoi = CDSE_json.get_aoi_string_from_geojson(area, decimals=4)

# -------------------------------------------------------------------------- #

    # build the query url

    # general query parameters

    # sensor
    querySTR_sensor = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{sensor}'"
    logger.debug(f"querySTR_sensor: {querySTR_sensor}")

    # area
    querySTR_area =  " and " + f"OData.CSC.Intersects(area=geography'SRID=4326;{aoi}')"
    logger.debug(f"querySTR_area: {querySTR_area}")

    # date and time
    querySTR_time = " and " + f"ContentDate/Start gt {start_date}T{start_time}.000Z and ContentDate/Start lt {end_date}T{end_time}.000Z"
    logger.debug(f"querySTR_time: {querySTR_time}")

    # ------------------------ #

    # processing level
    if processing_level is not None:

        if sensor == 'SENTINEL-1' and processing_level in [0,'0',1,'1']:
            querySTR_level = " and " + f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'processingLevel' and att/OData.CSC.StringAttribute/Value eq 'LEVEL{processing_level}')"

        elif sensor == 'SENTINEL-2' and processing_level in ['1C','2A']:
            querySTR_level = " and " + f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'processingLevel' and att/OData.CSC.StringAttribute/Value eq 'S2MSI{processing_level}')"

        else:
            logger.error(f"Processing level '{processing_level}' not valid for sensor '{sensor}'. Should have been caught by parameter check")

    else:
        querySTR_level = ""

    logger.debug(f"querySTR_level: {querySTR_level}")

    # ------------------------ #




    # product type
    if product_type is not None:

        if sensor == 'SENTINEL-1' and product_type in ['GRD']:
            querySTR_product_type = " and " + f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq '*{product_type}*')"

        elif sensor == 'SENTINEL-2' and product_type in ['1C','2A']:
            querySTR_product_type = " and " + f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq 'S2MSI{product_type}')"

        else:
            logger.error(f"Product type '{productType}' not valid for sensor '{sensor}'. Should have been caught by parameter check")

    else:
        querySTR_product_type = ""

    logger.debug(f"querySTR_product_type: {querySTR_product_type}")






    # ------------------------ #

    # Sentinel-1 parameters

    if sensor == 'SENTINEL-1':

        # mode
        if sensor_mode is not None:
            querySTR_mode = " and " + f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'operationalMode' and att/OData.CSC.StringAttribute/Value eq '{sensor_mode}')"
    else:
        querySTR_mode = ""

    logger.debug(f"querySTR_mode: {querySTR_mode}")

    # ------------------------ #

    # Sentinel-2 parameters

    if sensor == 'SENTINEL-2':

        # cloud cover
        querySTR_max_cloud = " and " + f"Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value le {max_cloud_cover})"
    else:
        querySTR_max_cloud = ""


    logger.debug(f"querySTR_max_cloud: {querySTR_max_cloud}")

    # ------------------------ #

    # additional search parameters

    if expand_attributes:
        querySTR_expand_attributes = "&$expand=Attributes"
    else:
        querySTR_expand_attributes = ""
    logger.debug(f"querySTR_expand_attributes: {querySTR_expand_attributes}")


    # max results
    querySTR_max_results = f"&$top={max_results}"
    logger.debug(f"querySTR_max_results: {querySTR_max_results}")

    # ------------------------ #

    # build full query string
    querySTR = f"{querySTR_sensor}{querySTR_area}{querySTR_max_cloud}{querySTR_mode}{querySTR_product_type}{querySTR_level}{querySTR_time}{querySTR_expand_attributes}{querySTR_max_results}"

    logger.info(f"Full query url: {querySTR}")

# -------------------------------------------------------------------------- #

    # search the data collection
    response_json = requests.get(querySTR).json()

    # extract list of products 
    product_list = response_json['value']

    logger.info(f"Query found {len(product_list)} products")

    if max_results<=len(product_list):
        logger.info(f"Number of products exceeds maximum number")
        logger.info(f"Access next query url at 'response_json['@odata.nextLink']")

    return response_json

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

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

# ---- End of <search_and_download.py> ----
