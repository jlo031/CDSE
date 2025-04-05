# ---- This is <test_aoi_functions.py> ----

"""
Test CDSE module aoi to wkt functions.
"""

import pathlib
from loguru import logger

import CDSE.json_utils as CDSE_json
import CDSE.utils as CDSE_utils
import CDSE.search_and_download as CDSE_sd
import CDSE.access_token_credentials as CDSE_atc

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

print("\n\n-------------------------------------------")
print("---- TEST READING AOI WKT FROM GEOJSON ----")
print("-------------------------------------------\n")

geojson_file_list = [
    'roi_hinlopen.geojson',
    'roi_multiple.geojson',
    'roi_svalbard.geojson',
    'roi_points.geojson',
    'roi_point_svalbard.geojson',
    'roi_point_antarctica.geojson',
]

for geojson_file in geojson_file_list:

    logger.info(f"Testing AOI extraction from: {geojson_file}")

    aoi = CDSE_json.get_aoi_string_from_geojson(geojson_file, decimals=3)

    print(f"{aoi}\n")

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

print("\n\n-------------------------------------------")
print("---- TEST READING AOI WKT FROM LAT/LON ----")
print("-------------------------------------------\n")

L = dict()
L['lat'] = 80.461723
L['lon'] = -15.00032

aoi = CDSE_json.get_aoi_string_from_lat_lon_dict(L, decimals=4)

print(f"{aoi}\n")

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <test_aoi_functions.py> ----
