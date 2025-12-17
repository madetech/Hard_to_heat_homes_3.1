from src.building_collection import BuildingCollection

bristol_bbox = {
      "minx": -3.117815916947311,
      "miny": 51.34162559147916,
      "maxx": -2.510419161285424,
      "maxy": 51.54443273743301
    }

bristol_bbox_string = str(bristol_bbox["minx"]) + str(bristol_bbox["miny"]) + str(bristol_bbox["maxx"]) + str(bristol_bbox["maxy"])

def test_produce_list_returns_an_empty_list_if_desired_list_length_is_zero():
    assert BuildingCollection(bristol_bbox_string, 0).produce_list() == []
def test_produce_list_returns_list_of_100_properties_if_desired_list_length_is_100():
    assert len(BuildingCollection(bristol_bbox_string, 100).produce_list()) == 100