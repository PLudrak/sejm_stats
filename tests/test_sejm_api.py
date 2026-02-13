import pytest
from unittest.mock import patch, Mock
from app.services.sejm_api import (
    get_all_deputies,
    get_deputy_details,
    fetch_votings,
    fetch_voting_details,
    map_voting_details,
    get_all_voting_results,
    SEJM_URL,
)


@patch("app.services.sejm_api.requests.get")
def test_get_all_deputies(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "accusativeName": "Andrzeja Adamczyka",
            "active": True,
            "birthDate": "1959-01-04",
            "birthLocation": "Krzeszowice",
            "club": "PiS",
            "districtName": "Kraków",
            "districtNum": 13,
            "educationLevel": "wyższe",
            "email": "Andrzej.Adamczyk@sejm.pl",
            "firstLastName": "Andrzej Adamczyk",
            "firstName": "Andrzej",
            "genitiveName": "Andrzeja Adamczyka",
            "id": 1,
            "lastFirstName": "Adamczyk Andrzej",
            "lastName": "Adamczyk",
            "numberOfVotes": 45171,
            "profession": "ekonomista",
            "secondName": "Mieczysław",
            "voivodeship": "małopolskie",
        }
    ]
    mock_get.return_value = mock_response

    result = get_all_deputies()

    assert isinstance(result, list)
    assert result[0]["name"] == "Andrzej Adamczyk"
    mock_get.assert_called_once()


@patch("app.services.sejm_api.requests.get")
def test_get_posel_details(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "accusativeName": "Andrzeja Adamczyka",
        "active": True,
        "birthDate": "1959-01-04",
        "birthLocation": "Krzeszowice",
        "club": "PiS",
        "districtName": "Kraków",
        "districtNum": 13,
        "educationLevel": "wyższe",
        "email": "Andrzej.Adamczyk@sejm.pl",
        "firstLastName": "Andrzej Adamczyk",
        "firstName": "Andrzej",
        "genitiveName": "Andrzeja Adamczyka",
        "id": 1,
        "lastFirstName": "Adamczyk Andrzej",
        "lastName": "Adamczyk",
        "numberOfVotes": 45171,
        "profession": "ekonomista",
        "secondName": "Mieczysław",
        "voivodeship": "małopolskie",
    }
    mock_get.return_value = mock_response

    result = get_deputy_details(1)

    assert result["id"] == 1
    assert result["club"] == "PiS"
    mock_get.assert_called_once_with("https://api.sejm.gov.pl/sejm/term10/MP/1")


@patch("app.services.sejm_api.requests.get")
def test_fetch_votings_calls_correct_url(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    fetch_votings(1)

    mock_get.assert_called_once_with(f"{SEJM_URL}/votings/1")


@patch("app.services.sejm_api.requests.get")
def test_fetch_voting_details_calls_correct_url(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    fetch_voting_details(1, 4)

    mock_get.assert_called_once_with(f"{SEJM_URL}/votings/1/4")


def test_map_voting_details():
    details = {
        "votes": [
            {"MP": "1", "vote": "YES"},
            {"MP": "2", "vote": "NO"},
        ]
    }

    result = map_voting_details(1, 4, details)

    assert result == {
        "sitting": 1,
        "voting": 4,
        "votes": {
            "1": "YES",
            "2": "NO",
        },
    }


@patch("app.services.sejm_api.fetch_voting_details")
@patch("app.services.sejm_api.fetch_votings")
def test_get_all_voting_results(mock_fetch_votings, mock_fetch_voting_details):

    # all votings of the sitting
    mock_fetch_votings.return_value = [
        {
            "votingNumber": 4,
            "sitting": 1,
            "kind": "ELECTRONIC",
        }
    ]

    # details of the voting
    mock_fetch_voting_details.return_value = {
        "votes": [
            {"MP": "1", "vote": "YES"},
            {"MP": "2", "vote": "NO"},
        ]
    }

    result = get_all_voting_results(1)

    assert result == [
        {
            "sitting": 1,
            "voting": 4,
            "votes": {
                "1": "YES",
                "2": "NO",
            },
        }
    ]

    mock_fetch_votings.assert_called_once_with(1)
    mock_fetch_voting_details.assert_called_once_with(1, 4)
