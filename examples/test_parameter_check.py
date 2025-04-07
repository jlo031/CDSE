# ---- This is <test_parameter_check.py> ----

"""
Test CDSE module parameter check.
"""

import pathlib
from loguru import logger

import CDSE.json_utils as CDSE_json
import CDSE.utils as CDSE_utils
import CDSE.search_and_download as CDSE_sd
import CDSE.access_token_credentials as CDSE_atc

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

print("\n\n--------------------------------")
print("---- TEST PARAMETER CHECK 1 ----")
print("--------------------------------\n")

# Adjust parameters to test propper functionality

data_collection = "SENTINEL-2"
geojson_path = 'ROIs/roi_svalbard.geojson'
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
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

print("\n\n--------------------------------")
print("---- TEST PARAMETER CHECK 2 ----")
print("--------------------------------\n")

# Adjust parameters to test propper functionality

data_collection = "SENTINEL-1"
geojson_path = 'ROIs/roi_svalbard.geojson'
start_date = "2022-06-01"
end_date = "2022-06-06"
start_time = "02:00:00"
end_time = "15:00:00"
sensor_mode = 'IW'
processing_level = '1'
product_type = 'GRD'
max_cloud_cover = 100
max_results = 1000
expand_attributes = 5,
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

# ---- End of <test_parameter_check.py> ----
