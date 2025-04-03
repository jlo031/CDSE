# ---- This is <test_1.py> ----

"""
Test CDSE module
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

print("\n-------------------------------------------")
print("---- TEST READING AOI WKT FROM GEOJSON ----")
print("-------------------------------------------\n")

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

print("\n------------------------------")
print("---- TEST PARAMETER CHECK ----")
print("------------------------------\n")

# Adjust parameters to test propper functionality

data_collection = "SENTINEL-2"
geojson_path = 'roi_svalbard.geojson'
start_date = "2022-06-01"
end_date = "2022-06-06"
start_time = "02:00:00"
end_time = "15:00:00"
sensor_mode = 'EW'
processing_level = '1C'
product_type = '1C'
max_cloud_cover = 100
max_results = 1000
expand_attributes = True
loglevel = 'DEBUG'

# check the parameters defined above
status = CDSE_sd.check_CDSE_request_parameters(
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

logger.info(f"Parameter check status is '{status}'\n")

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <test_1.py> ----
