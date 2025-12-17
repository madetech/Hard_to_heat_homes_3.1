from src.os_api import os_api_call
from src.variables import OS_KEY

class BuildingCollection:
    HEADERS = {"Accept": "application/json"}
    FILTER = "buildinguse_oslandusetiera = 'Residential Accommodation' AND mainbuildingid_ismainbuilding = 'Yes'"
    def __init__(self, council_bbox, pages):
        self.council_bbox = council_bbox
        self.pages = pages
        self.params = {
            "key": OS_KEY,
            "filter" : BuildingCollection.FILTER,
            "bbox": self.council_bbox,
            "offset": 0
            }
    def produce_list(self):
        list_of_buildings = []
        while self.pages > 0:
            list_of_buildings += os_api_call(BuildingCollection.HEADERS, self.params)["features"]
            self.pages -= 1
            self.params["offset"] += 100 
        return list_of_buildings