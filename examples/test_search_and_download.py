# ---- This is <test_search_and_download.py> ----

"""
Test search and download of S1 data from CDSE.
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

print("\n\n-------------------------------------------------")
print("---- TEST CDSE CATALOGUE QUERY FROM LAT/LON ----")
print("------------------------------------------------\n")

data_collection = "Sentinel-1"
L = dict()
L['lat'] = 80.461723
L['lon'] = -15.00032
start_date = "2022-06-02"
end_date = "2022-06-04"
start_time = "02:00:00"
end_time = "15:00:00"
sensor_mode = 'EW'
processing_level = '1'
product_type = 'GRD'
max_cloud_cover = 100
max_results = 100
expand_attributes = True
loglevel = 'INFO'

response_json = CDSE_sd.search_CDSE_catalogue(
    sensor = data_collection,
    area = L,
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

product_name_list = CDSE_utils.get_product_names_from_response_json(response_json)
logger.info(f"List of found product: \n        {"\n        ".join(product_name_list)}")

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

print("\n\n------------------------------------------------")
print("---- TEST CDSE CATALOGUE QUERY FROM GEOJSON ----")
print("------------------------------------------------\n")

data_collection = "Sentinel-1"
geojson_path = 'ROIs/roi_point_svalbard.geojson'
geojson_path = 'ROIs/roi_point_antarctica.geojson'
geojson_path = 'ROIs/roi_points.geojson'

start_date = "2022-06-02"
end_date = "2022-06-04"
start_time = "02:00:00"
end_time = "15:00:00"
sensor_mode = 'EW'
processing_level = '1'
product_type = 'GRD'
max_cloud_cover = 100
max_results = 100
expand_attributes = True
loglevel = 'INFO'

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

product_name_list = CDSE_utils.get_product_names_from_response_json(response_json)
logger.info(f"List of found product: \n        {"\n        ".join(product_name_list)}")

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

print("\n\n--------------------------------------------------------")
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

print("\n\n--------------------------------------")
print("---- TEST CDSE CATALOGUE DOWNLOAD ----")
print("--------------------------------------\n")

# get username and password from local .env file
CDSE_user, CDSE_passwd = CDSE_utils.get_user_and_passwd(dotenv_path = '.env')

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

# ---- End of <test_search_and_download.py> ----
