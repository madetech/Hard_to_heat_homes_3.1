from tests.test_data.epc_dummy_data import epc_dummy_data
from src.epc_api import epc_api_call
from src.os_api import os_api_call
from src.property import Property
from src.utils import get_properties_from_os
from src.variables import EPC_TOKEN, OS_KEY
import json 
import pytest

with open("tests/test_data/os_dummy_data.json", "r") as data:
    os_dummy_data = json.load(data)

EPC_PARAMS = "uprn=200002791"
EPC_HEADERS = {"Accept": "application/json", "Authorization": f"Basic {EPC_TOKEN}"}

OS_HEADERS = {"Accept": "application/json"}
OS_PARAMS = {
        "key": OS_KEY,
        "limit": 3,
        "filter": "oslandusetiera LIKE 'Residential Accommodation' AND ismainbuilding=true",
        "bbox": "-0.372438,51.405655,-0.371885,51.40600",
         }

@pytest.fixture
def mock_epc_api_call(mocker):
    mock_get = mocker.patch("src.epc_api.requests.get")
    mock_response = mock_get.return_value
    mock_response.json.return_value = epc_dummy_data
    result = epc_api_call(EPC_HEADERS, EPC_PARAMS)
    return result

def test_property_has_uprn():
    dummy_property = Property("200002791")
    assert dummy_property.uprn == "200002791"


def test_property_has_uprn_from_dummy_data():
    dummy_property = Property(epc_dummy_data["rows"][0]["uprn"])
    assert dummy_property.uprn == "200002791"


def test_property_has_uprn_from_mock_api_call(mock_epc_api_call):
    dummy_property = Property(mock_epc_api_call["rows"][0]["uprn"])
    assert dummy_property.uprn == "200002791"


def test_property_has_EPC_rating():
    dummy_property = Property("200002791")
    dummy_property.epc_rating = "D"
    assert dummy_property.epc_rating == "D"


def test_property_has_correct_attributes_from_mock_api_call(mock_epc_api_call):
    dummy_property = Property(
        mock_epc_api_call["rows"][0]["uprn"]
    )
    dummy_property.epc_rating = "D"
    dummy_property.uprn = "200002791"
    dummy_property.epc_score = "63"
    dummy_property.address = "30 Alexandra Road, Muswell Hill, N10 2RT"
    dummy_property.energy_usage = "314"
    assert dummy_property.epc_rating == "D"
    assert dummy_property.uprn == "200002791"
    assert dummy_property.epc_score == "63"
    assert dummy_property.address == "30 Alexandra Road, Muswell Hill, N10 2RT"
    assert dummy_property.energy_usage == "314"

def test_get_properties_from_os_updates_property_data(mocker):
    mock_get = mocker.patch("src.os_api.requests.get")
    mock_response = mock_get.return_value
    mock_response.json.return_value = os_dummy_data

    buildings = os_api_call(OS_HEADERS, OS_PARAMS)[0]["features"] #dummy data
    properties = get_properties_from_os(buildings)

    dummy_building = buildings[0]["properties"]
    dummy_property = properties[0] 

    assert dummy_property.age == dummy_building["buildingage_period"]
    assert dummy_property.connectivity == dummy_building["connectivity"]
    assert dummy_property.material == dummy_building["constructionmaterial"]
    assert dummy_property.building_id == dummy_building["sitereference"][0]["buildingid"]



