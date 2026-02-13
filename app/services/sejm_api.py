### getting data from sejm api

import requests

SEJM_URL = "https://api.sejm.gov.pl/sejm/term10"


def get_all_deputies():
    r = requests.get(f"{SEJM_URL}/MP", timeout=5)
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


def get_deputy_details(leg: int):
    r = requests.get(f"{SEJM_URL}/MP/{leg}")
    return r.json()


def fetch_votings(sitting: int):
    r = requests.get(f"{SEJM_URL}/votings/{sitting}")
    r.raise_for_status()
    return r.json()


def map_voting_list(data):
    return [{"voting_no": v["votingNumber"], "sitting": v["sitting"]} for v in data]


def fetch_voting_details(sitting: int, voting: int):
    r = requests.get(f"{SEJM_URL}/votings/{sitting}/{voting}")
    r.raise_for_status()
    return r.json()


def map_voting_details(sitting: int, voting_no: int, details: dict):
    votes = {vote["MP"]: vote["vote"] for vote in details["votes"]}

    return {
        "sitting": sitting,
        "voting": voting_no,
        "votes": votes,
    }


def get_all_voting_results(sitting: int):
    raw_votings = fetch_votings(sitting)
    mapped_votings = map_voting_list(raw_votings)

    results = []
    for voting in mapped_votings:
        voting_no = voting["voting_no"]
        details = fetch_voting_details(sitting, voting_no)
        results.append(map_voting_details(sitting, voting_no, details))

    return results
