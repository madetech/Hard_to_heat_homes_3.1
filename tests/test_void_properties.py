from src.property import Property
from src.utils import get_properties_from_os
import json

with open("tests/test_data/os_dummy_data.json") as data:
    os_dummy_data = json.load(data)



# list_of_properties = get_properties_from_os(os_dummy_data['features'])
# setting_void_properties(list_of_properties)

# def test_property_has_void_status_false():
#     test_prop = Property(1)
#     assert test_prop.void == False

# def test_filters_for_void_properties():
#     void_properties = filter_for_void(list_of_properties)
#     assert void_properties[0].void == True
#     assert len(void_properties) == 2
    