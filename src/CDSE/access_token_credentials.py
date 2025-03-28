# ---- This is <access_token_credentials.py> ----

"""
Generate access token for CDSE.
"""

import requests

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

def get_access_token(username: str, password: str) -> str:
    """
    Get access token for CDSE.

    Parameters
    ----------
    username : CDSE username
    password : CDSE password

    Returns
    -------
    access_token : CDSE access token
    """

    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
    }

    try:
        r = requests.post(
            "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data = data,
        )
        r.raise_for_status()
    except Exception as e:
        raise Exception(f"Access token creation failed. Reponse from the server was: {r.json()}")

    return r.json()["access_token"]

##access_token = get_access_token("johannes.p.lohse@uit.no","Dummy_Password123")

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---- End of <access_token_credentials.py> ----
