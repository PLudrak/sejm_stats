### getting data from sejm api

import requests

SEJM_URL = "https://api.sejm.gov.pl/sejm/term10"


def get_all_deputies():
    r = requests.get(SEJM_URL, timeout=5)
    r.raise_for_status()
    data = r.json()
    return [
        {
            "id": dep["id"],
            "name": dep["firstLastName"],
            "club": dep["club"],
            "districtNum": dep["districtNum"],
        }
        for dep in data
    ]


def get_deputy_details(leg):
    r = requests.get(f"{SEJM_URL}/{leg}")
    return r.json()
