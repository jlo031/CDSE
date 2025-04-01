# ---- This is <usage_examples.py> ----

"""
Example for search and download of S1 data from CDSE.

https://documentation.dataspace.copernicus.eu/APIs/OData.html

https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name%20eq%20'SENTINEL-1'%20and%20OData.CSC.Intersects(area=geography'SRID=4326;POLYGON((4.220581%2050.958859,4.521264%2050.953236,4.545977%2050.906064,4.541858%2050.802029,4.489685%2050.763825,4.23843%2050.767734,4.192435%2050.806369,4.189689%2050.907363,4.220581%2050.958859))')%20and%20ContentDate/Start%20gt%202022-06-01T00:00:00.000Z%20and%20ContentDate/Start%20lt%202022-06-10T00:00:00.000Z
https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name%20eq%20%27CCM%27%20and%20ContentDate/Start%20gt%202005-05-03T00:00:00.000Z%20and%20ContentDate/Start%20lt%202022-05-03T00:11:00.000Z
https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name%20eq%20%27SENTINEL-2%27%20and%20Attributes/OData.CSC.DoubleAttribute/any(att:att/Name%20eq%20%27cloudCover%27%20and%20att/OData.CSC.DoubleAttribute/Value%20le%2040.00)%20and%20ContentDate/Start%20gt%202022-01-01T00:00:00.000Z%20and%20ContentDate/Start%20lt%202022-01-03T00:00:00.000Z&$top=10
https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq 'SENTINEL-1' and Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq 'EW_GRDM_1S') and ContentDate/Start gt 2022-05-03T00:00:00.000Z and ContentDate/Start lt 2022-05-03T12:00:00.000Z&$top=100
"""


import sys
import pathlib
from loguru import logger

import CDSE.json_utils as CDSE_json
import CDSE.CDSE_search_and_download as CDSE_sd

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# DEFINE INPUT PARAMETERS

# area
geojson_path = 'roi_svalbard.geojson'

# date and time
start_date = "2022-06-01"
end_date = "2022-06-02"
start_time = "02:00:00"
end_time = "15:00:00"

# sensor
data_collection = "SENTINEL-1"
data_collection = "SENTINEL-2"

# mode
sensor_mode = 'IW'

# processing_level
processing_level = 1

# maximum cloud cover
max_cloud = 100

# maximum  items per query
max_results = 1000

expand_attributes = True

loglevel = 'DEBUG'

# get username and password
CDSE_user = "johannes.p.lohse@uit.no"
CDSE_passwd = "Dummy_Password123"

# download dir
download_dir = "/home/jo/temporary_downloads"

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ------------------------------------------- #
# ---- TEST READING AOI WKT FROM GEOJSON ---- #
# ------------------------------------------- #

geojson_file_list = [
    'roi_hinlopen.geojson',
    'roi_multiple.geojson',
    'roi_svalbard.geojson',
]

for geojson_file in geojson_file_list:

    logger.info(f"Testing AOI extraction from: {geojson_file}")

    aoi = CDSE_json.get_aoi_string_from_geojson(geojson_file, decimals=3)

    print(f"{aoi}\n")

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ------------------------------ #
# ---- TEST PARAMETER CHECK ---- #
# ------------------------------ #

# adjsut individual parameters to check that errors are caught
# for example
status = CDSE_sd.check_CDSE_request_parameters(
    sensor = data_collection,
    area = geojson_path,
    start_date = 'false_input',
    end_date = end_date,
)
logger.info(f"Parameter check status is '{status}'\n")


# check the parameters defined above
status = CDSE_sd.check_CDSE_request_parameters(
    sensor = data_collection,
    area = geojson_path,
    start_date = start_date,
    end_date = end_date,
    start_time = start_time,
    end_time = end_time,
    max_results = max_results,
    max_cloud_cover = max_cloud,
    sensor_mode = sensor_mode,
    processing_level = processing_level,
    expand_attributes = expand_attributes,
    loglevel = loglevel
)
logger.info(f"Parameter check status is '{status}'\n")





















# check the parameters defined above
status = CDSE_sd.check_CDSE_request_parameters(
    sensor = 'Sentinel-1',
    area = geojson_path,
    start_date = start_date,
    end_date = end_date,
    start_time = start_time,
    end_time = end_time,
    max_results = max_results,
    max_cloud_cover = max_cloud,
    sensor_mode = sensor_mode,
    processing_level = 1,
    expand_attributes = expand_attributes,
    loglevel = loglevel
)
logger.info(f"Parameter check status is '{status}'\n")













# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# -------------------------- #
# ---- TEST CDSE SEARCH ---- #
# -------------------------- #

logger.info("Testing CDSE catalogue query")

response_json = CDSE_sd.search_CDSE_catalogue(
    sensor = data_collection,
    area = geojson_path,
    start_date = start_date,
    end_date = end_date,
    start_time = start_time,
    end_time = end_time,
    max_results = 200,
    max_cloud_cover = max_cloud,
    sensor_mode = sensor_mode,
    processing_level = 2,
    expand_attributes = expand_attributes,
    loglevel = loglevel
)

logger.info(f"'response_json' has keys: {response_json.keys()}")

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

sys.exit()

# ---------------------------- #
# ---- TEST CDSE DOWNLOAD ---- #
# ---------------------------- #

logger.info("Testing CDSE catalogue download")

# get product_list from response_json
product_list = response_json['value']

# make sure download_dir exists
download_dir = pathlib.Path(download_dir).resolve()
download_dir.mkdir(mode=511, parents=False, exist_ok=True)

CDSE_sd.download_product_list_from_cdse(
    product_list,
    download_dir,
    username = CDSE_user,
    password = CDSE_passwd,
    overwrite=False,
    chunk_size=8192,
)

sys.exit()

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #


# Check found products

logger.info(f"Found {len(product_list)} data products")

# initiate individual product lists
IW_GRD_product_list = []
EW_GRD_product_list = []
IW_RAW_product_list  = []
IW_SLC_product_list  = []
EW_RAW_product_list  = []
EW_SLC_product_list  = []
MISC_product_list    = []

for i, result in enumerate(product_list):
    ##logger.debug(f"Checking product {i+1} of {len(product_list)}")
    ##logger.debug(f"Name: {result['Name']}")
    ##logger.debug(f"Id:   {result['Id']}")

    if 'IW_GRD' in result['Name']:
        ##logger.debug('Adding current product to IW_GRD list')
        IW_GRD_product_list.append(result)

    elif 'EW_GRD' in result['Name']:
        ##logger.debug('Adding current product to EW_GRD list')
        EW_GRD_product_list.append(result)


    elif 'IW_RAW' in result['Name']:
        ##logger.debug('Adding current product to IW_RAW list')
        IW_RAW_product_list.append(result)

    elif 'IW_SLC' in result['Name']:
        ##logger.debug('Adding current product to IW_RAW list')
        IW_SLC_product_list.append(result)


    elif 'EW_RAW' in result['Name']:
        ##logger.debug('Adding current product to EW_RAW list')
        EW_RAW_product_list.append(result)

    elif 'EW_SLC' in result['Name']:
        ##logger.debug('Adding current product to EW_RAW list')
        EW_SLC_product_list.append(result)

    else:
        ##logger.debug('Adding current product to misc product list')
        MISC_product_list.append(result)

    ##print('')

logger.info(f"IW GRD products: {len(IW_GRD_product_list)}")
logger.info(f"EW GRD products: {len(EW_GRD_product_list)}")
logger.info(f"IW RAW products: {len(IW_RAW_product_list)}")
logger.info(f"IW SLC products: {len(IW_SLC_product_list)}")
logger.info(f"EW RAW products: {len(EW_RAW_product_list)}")
logger.info(f"EW SLC products: {len(EW_SLC_product_list)}")
logger.info(f"MISC products:   {len(MISC_product_list)}")


sys.exit()


for i, result in enumerate(IW_GRD_product_list):
    logger.debug(f"Checking product {i+1} of {len(IW_GRD_product_list)}")
    logger.debug(f"Name: {result['Name']}")
    logger.debug(f"Id:   {result['Id']}")
    print('')

for i, result in enumerate(EW_GRD_product_list):
    logger.debug(f"Checking product {i+1} of {len(EW_GRD_product_list)}")
    logger.debug(f"Name: {result['Name']}")
    logger.debug(f"Id:   {result['Id']}")
    print('')

for i, result in enumerate(IW_SLC_product_list):
    logger.debug(f"Checking product {i+1} of {len(IW_SLC_product_list)}")
    logger.debug(f"Name: {result['Name']}")
    logger.debug(f"Id:   {result['Id']}")
    print('')

for i, result in enumerate(IW_RAW_product_list):
    logger.debug(f"Checking product {i+1} of {len(IW_RAW_product_list)}")
    logger.debug(f"Name: {result['Name']}")
    logger.debug(f"Id:   {result['Id']}")
    print('')

for i, result in enumerate(EW_SLC_product_list):
    logger.debug(f"Checking product {i+1} of {len(EW_SLC_product_list)}")
    logger.debug(f"Name: {result['Name']}")
    logger.debug(f"Id:   {result['Id']}")
    print('')

for i, result in enumerate(EW_RAW_product_list):
    logger.debug(f"Checking product {i+1} of {len(EW_RAW_product_list)}")
    logger.debug(f"Name: {result['Name']}")
    logger.debug(f"Id:   {result['Id']}")
    print('')

for i, result in enumerate(MISC_product_list):
    logger.debug(f"Checking product {i+1} of {len(MISC_product_list)}")
    logger.debug(f"Name: {result['Name']}")
    logger.debug(f"Id:   {result['Id']}")
    print('')

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <usage_examples.py> ----
