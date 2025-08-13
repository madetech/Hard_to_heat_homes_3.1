from src.property import Property
from tests.test_data.new_epc_dummy_data import epc_dummy_data

def test_get_attributes_from_epc_updates_property_addresses(mocker):
    mocked_api_call = mocker.patch("src.utils.epc_api_call_address", return_value = epc_dummy_data)
    from src.utils import get_attributes_from_epc
    properties = [Property("10033322697"),
                    Property("10033322698"),
                    Property("100061342030"),
                    Property("1")]
    
    properties = get_attributes_from_epc(properties)

    mocked_api_call.assert_called_once()
    assert properties[0].address == "13c Wilton Gardens, Surrey, KT8 1QP"
    assert properties[1].address == "13b, Wilton Gardens, Surrey, KT8 1QP"
    assert properties[2].address == "13a, Wilton Gardens, Surrey, KT8 1QP"
    assert properties[3].address == ""

def test_get_attributes_from_epc_api_returns_false(mocker):
    mocked_api_call = mocker.patch("src.utils.epc_api_call_address", return_value = False)
    from src.utils import get_attributes_from_epc
    properties = [Property("10033322697"),
                    Property("10033322698"),
                    Property("100061342030"),
                    Property("1")]

    properties = get_attributes_from_epc(properties)

    mocked_api_call.assert_called_once()
    assert properties[0].address == ""
    assert properties[1].address == ""
    assert properties[2].address == ""
    assert properties[3].address == ""


def test_get_attributes_from_epc_does_batching(mocker):
    mocked_api_call = mocker.patch("src.utils.epc_api_call_address", return_value = epc_dummy_data)
    from src.utils import get_attributes_from_epc
    properties = [Property(str(i)) for i in range(120)]
    
    properties = get_attributes_from_epc(properties)

    assert mocked_api_call.call_count == 3

def test_get_remaining_attributes_from_epc(mocker):
    mocked_api_call = mocker.patch("src.utils.epc_api_call_address", return_value = epc_dummy_data)
    from src.utils import get_attributes_from_epc
    properties = [Property("10033322697"),
                    Property("10033322698"),
                    Property("100061342030"),
                    Property("1")]
    
    properties = get_attributes_from_epc(properties)

    mocked_api_call.assert_called_once()
    assert properties[0].epc_rating == "D"
    assert properties[0].epc_score == "63"
    assert properties[0].energy_usage == "220"
    assert properties[1].epc_rating == "B"
    assert properties[1].epc_score == "86"
    assert properties[1].energy_usage == "62"
    
    assert properties[3].epc_rating == "No Rating Found"
    assert properties[3].epc_score == "No Score Found"
    assert properties[3].energy_usage == "No Usage Found"