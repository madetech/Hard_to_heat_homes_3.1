from src.council_data_utils import filter_properties_by_council_code, load_uprn_to_council
from src.utils import get_properties_from_os
import json
from src.property import Property

with open("tests/test_data/os_dummy_data.json") as data:
    os_dummy_data = json.load(data)
    
array_of_buildings = []
for collection in os_dummy_data:
    array_of_buildings.extend(collection["features"])

props = get_properties_from_os(array_of_buildings)

def test_filter_properties_in_elmbridge():
    elmbridge_council_code = "E07000207"
    filtered_props = filter_properties_by_council_code(elmbridge_council_code, props)
    uprn_to_council_dict = load_uprn_to_council(elmbridge_council_code)

    assert all(uprn_to_council_dict[str(prop.uprn)] == elmbridge_council_code for prop in filtered_props)

def test_filter_properties_in_east_hampshire():
    east_hampshire_council_code = "E07000085"
    filtered_props = filter_properties_by_council_code(east_hampshire_council_code, props)
    uprn_to_council_dict = load_uprn_to_council(east_hampshire_council_code)

    assert all(uprn_to_council_dict[str(prop.uprn)] == east_hampshire_council_code for prop in filtered_props)

def test_filter_properties_in_tunbridge_wells():
    tunbridge_wells_council_code = "E07000116"
    filtered_props = filter_properties_by_council_code(tunbridge_wells_council_code, props)
    uprn_to_council_dict = load_uprn_to_council(tunbridge_wells_council_code)

    assert all(uprn_to_council_dict[str(prop.uprn)] == tunbridge_wells_council_code for prop in filtered_props)

def test_filter_properties_in_bristol():
    bristol_council_code = "E06000023"
    filtered_props = filter_properties_by_council_code(bristol_council_code, props)
    uprn_to_council_dict = load_uprn_to_council(bristol_council_code)

    assert all(uprn_to_council_dict[str(prop.uprn)] == bristol_council_code for prop in filtered_props)

def test_filter_properties_for_():
    filtered_props = filter_properties_by_council_code(None, props)

    assert filtered_props == []
