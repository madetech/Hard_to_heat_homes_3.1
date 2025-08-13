from src.property import Property
from src.utils import *
import json

with open("tests/test_data/os_dummy_data.json") as data:
    os_dummy_data = json.load(data)
    
array_of_buildings = os_dummy_data["features"]
props = get_properties_from_os(array_of_buildings)
uprn = "100061338652"

def test_returns_array_of_property_instances_from_os():
    assert type(props) is list
    assert type(props[0]) is Property

def test_properties_have_desired_attributes():
    assert props[0].connectivity == "Semi-Connected"
    assert props[0].age == "1945-1959"
    assert props[0].material == "Brick Or Block Or Stone"
    assert props[0].uprn == 100061342030
    assert props[1].uprn == 100061342031
    assert props[2].connectivity == "Multi-Connected"
    assert props[2].uprn == 10033322698
    assert props[2].age == 2012
    assert props[2].material == "Brick Or Block Or Stone"
    assert props[0].long == -0.3723468
    assert props[0].lat == 51.4059309
