import pytest
from unittest.mock import patch, Mock
from app.services.sejm_api import get_all_deputies, get_deputy_details


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
