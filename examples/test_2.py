# ---- This is <test_2.py> ----

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
import CDSE.utils as CDSE_utils
import CDSE.search_and_download as CDSE_sd
import CDSE.access_token_credentials as CDSE_atc

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

print("\n-----------------------------------")
print("---- TEST CDSE CATALOGUE QUERY ----")
print("-----------------------------------\n")

data_collection = "Sentinel-1"
geojson_path = 'roi_svalbard.geojson'
start_date = "2022-06-01"
end_date = "2022-06-06"
start_time = "02:00:00"
end_time = "15:00:00"
sensor_mode = None
processing_level = '1'
product_type = 'SLC'
max_cloud_cover = 100
max_results = 8
expand_attributes = True
loglevel = 'DEBUG'

response_json = CDSE_sd.search_CDSE_catalogue(
    sensor = data_collection,
    area = geojson_path,
    start_date = start_date,
    end_date = end_date,
    start_time = start_time,
    end_time = end_time,
    sensor_mode = sensor_mode,
    product_type = product_type,
    processing_level = processing_level,
    max_cloud_cover = max_cloud_cover,
    max_results = max_results,
    expand_attributes = expand_attributes,
    loglevel = loglevel
)

logger.info(f"'response_json' has keys: {response_json.keys()}")

for p in response_json['value']:
    print(f"{p['Name']}")

sys.exit()

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

print("\n--------------------------------------------------------")
print("---- TEST CDSE CATALOGUE QUERY FOR SPECIFIC PRODUCT ----")
print("--------------------------------------------------------\n")

example_product = "S1A_EW_GRDM_1SDH_20220602T073727_20220602T073831_043481_05310C_53F3.SAFE"
loglevel = 'INFO'

response_json = CDSE_sd.search_CDSE_catalogue_by_name(
    example_product,
    loglevel = loglevel
)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---------------------------- #
# ---- TEST CDSE DOWNLOAD ---- #
# ---------------------------- #

print("\n--------------------------------------")
print("---- TEST CDSE CATALOGUE DOWNLOAD ----")
print("--------------------------------------\n")


# get username and password
CDSE_user = "johannes.p.lohse@uit.no"
CDSE_passwd = "Dummy_Password123"

# download dir
download_dir = "/home/jo/temporary_downloads"

# make sure download_dir exists
download_dir = pathlib.Path(download_dir).resolve()
download_dir.mkdir(mode=511, parents=False, exist_ok=True)

# get product_list from response_json
product_list = list(response_json['value'])

CDSE_sd.download_product_list_from_cdse(
    product_list,
    download_dir,
    username = CDSE_user,
    password = CDSE_passwd,
    overwrite=False,
    chunk_size=8192,
)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <test_2.py> ----
