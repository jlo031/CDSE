# ---- This is <search_and_download_example.py> ----

"""
Example for search and download of S1 data from CDSE.

https://documentation.dataspace.copernicus.eu/APIs/OData.html

https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name%20eq%20'SENTINEL-1'%20and%20OData.CSC.Intersects(area=geography'SRID=4326;POLYGON((4.220581%2050.958859,4.521264%2050.953236,4.545977%2050.906064,4.541858%2050.802029,4.489685%2050.763825,4.23843%2050.767734,4.192435%2050.806369,4.189689%2050.907363,4.220581%2050.958859))')%20and%20ContentDate/Start%20gt%202022-06-01T00:00:00.000Z%20and%20ContentDate/Start%20lt%202022-06-10T00:00:00.000Z
https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name%20eq%20%27CCM%27%20and%20ContentDate/Start%20gt%202005-05-03T00:00:00.000Z%20and%20ContentDate/Start%20lt%202022-05-03T00:11:00.000Z
https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name%20eq%20%27SENTINEL-2%27%20and%20Attributes/OData.CSC.DoubleAttribute/any(att:att/Name%20eq%20%27cloudCover%27%20and%20att/OData.CSC.DoubleAttribute/Value%20le%2040.00)%20and%20ContentDate/Start%20gt%202022-01-01T00:00:00.000Z%20and%20ContentDate/Start%20lt%202022-01-03T00:00:00.000Z&$top=10

"""

import requests
import CDSE.access_token_credentials as CDSE_atc
import CDSE.CDSE_utils as CDSE_utils

import CDSE.geojson_utils as CDSE_geo

from loguru import logger

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# THIS SHOULD ALL BE USER INPUT DATA

# define path to geojson file for search area
geojson_path = 'roi_svalbard.geojson'
geojson_path = 'roi_multiple.geojson'

# define search parameters
start_date = "2022-06-01"
end_date = "2022-06-03"

# sensor
data_collection = "SENTINEL-1"

# maximum cloud cover
max_cloud = 65

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# read aoi from geojson path
aoi = CDSE_geo.geojson_to_wkt(CDSE_geo.read_geojson(geojson_path))

# manual example AOIs
##aoi = "POLYGON((4.220581 50.958859,4.521264 50.953236,4.545977 50.906064,4.541858 50.802029,4.489685 50.763825,4.23843 50.767734,4.192435 50.806369,4.189689 50.907363,4.220581 50.958859))"
##aoi = "POLYGON((-15 78, -10 78, -10 77, -15 77, -15 78))"


# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# BUILD THE QUERY URL

# build query string: sensor
query_string_sensor = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}'"

# build query string: area
query_string_area =  f"OData.CSC.Intersects(area=geography'SRID=4326;{aoi}')"

# build query string: time
query_string_time = f"ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T00:00:00.000Z"

# build full query string
query_string = f"{query_string_sensor} and {query_string_area} and {query_string_time}"

logger.info(f"Full quer string: {query_string}")


# search the data collection
response_dict = requests.get(query_string).json()



# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ONLY NEEDED FOR DOWNLOAD

# get username and password
CDSE_user = "johannes.p.lohse@uit.no"
CDSE_passwd = "Dummy_Password123"

# generate access token (for download)
access_token = CDSE_atc.get_access_token(CDSE_user, CDSE_passwd)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #






# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #










##query_string_test = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') and ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T00:00:00.000Z"




# S1 with area polygon and start/end date
response_dict = requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') and ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T00:00:00.000Z").json()

# S2 with area polygon, start/end date, cloud cover
response_dict = requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') and ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T00:00:00.000Z and Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value le {max_cloud})").json()

response_list = response_dict['value']

logger.info(f"Found {len(response_list)} data products")

# initiate individual product lists
IW_GRDH_product_list = []
IW_RAW_product_list  = []
IW_SLC_product_list  = []
MISC_product_list    = []

for i, result in enumerate(response_list):
    logger.debug(f"Checking product {i+1} of {len(response_list)}")
    logger.debug(f"Name: {result['Name']}")
    logger.debug(f"Id:   {result['Id']}")

    if 'IW_GRDH' in result['Name']:
        logger.debug('Adding current product to IW_GRDH list')
        IW_GRDH_product_list.append(result)

    elif 'IW_RAW' in result['Name']:
        logger.debug('Adding current product to IW_RAW list')
        IW_RAW_product_list.append(result)

    elif 'IW_SLC' in result['Name']:
        logger.debug('Adding current product to IW_RAW list')
        IW_SLC_product_list.append(result)

    else:
        logger.debug('Adding current product to misc product list')
        MISC_product_list.append(result)

    print('')

logger.info(f"IW GRDH products: {len(IW_GRDH_product_list)}")
logger.info(f"IW RAW products:  {len(IW_RAW_product_list)}")
logger.info(f"IW SLC products:  {len(IW_SLC_product_list)}")
logger.info(f"MISC products:    {len(MISC_product_list)}")


"""
for i, result in enumerate(IW_GRDH_product_list):
    logger.debug(f"Checking product {i+1} of {len(IW_GRDH_product_list)}")
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
"""





# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <search_and_download_example.py> ----


import pandas as pd

json = requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') and ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T00:00:00.000Z").json()


result_list = json['value']


for i,result in enumerate(result_list):
    print(i)
    print(result['Name'])
    print(result['Id'])
    print('')

pd.DataFrame.from_dict(json['value']).head(5)






url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({result['Id']})/$value"

headers = {"Authorization": f"Bearer {access_token}"}

session = requests.Session()
session.headers.update(headers)
response = session.get(url, headers=headers, stream=True)

with open(f"{result['Name'].split('.SAFE')[0]}.zip", "wb") as file:
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            file.write(chunk)



# for batch download:
# explicitly close session and response after each download
# maybe generate new token
