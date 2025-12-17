from src.building_collection import BuildingCollection
import pytest

bristol_bbox = {
      "minx": -3.117815916947311,
      "miny": 51.34162559147916,
      "maxx": -2.510419161285424,
      "maxy": 51.54443273743301
    }

bristol_bbox_string = str(bristol_bbox["minx"]) + str(bristol_bbox["miny"]) + str(bristol_bbox["maxx"]) + str(bristol_bbox["maxy"])    

@pytest.mark.parametrize(
        "bbox, pages, expected_length",
        [(bristol_bbox_string, 0, 0), (bristol_bbox_string, 1, 100), (bristol_bbox_string, 2, 200)])
def test_produce_list_returns_list_of_correct_length_based_on_pages(bbox, pages, expected_length):
    assert len(BuildingCollection(bbox, pages).produce_list()) == expected_length

def test_list_items_are_dictionaries():
    collection = BuildingCollection(bristol_bbox_string, 1).produce_list()
    for item in collection:
        assert type(item) == dict