import geopandas as gpd
import pandas as pd
import json
from shapely.geometry import shape
# from src.epc_api import epc_api_call_address

with open("data/councils_bbox_data_DEMO.json") as bbox_json:
    councils_data = json.load(bbox_json)

"""
Add in your census code as a key and pair it to the relevant CSV file
in your project directory as the value
"""

COUNCIL_CSV_MAP = {

    "E06000023": "data/uprn_to_council_SW.csv",   # Bristol
    "default": "data/uprn_to_council_data_SE_DEMO.csv" # South East Data Set
}

def load_uprn_to_council(council_code):
    """
    Load the correct UPRN to Council mapping based on council_code.
    Defaults to SE unless user selects Bristol.

    """
    csv_file = COUNCIL_CSV_MAP.get(council_code, COUNCIL_CSV_MAP["default"])
    df = pd.read_csv(csv_file, dtype={"UPRN": str, "COUNCIL_CODE": str})
    return pd.Series(df.COUNCIL_CODE.values, index=df.UPRN).to_dict()


def get_bbox_for_council_code(council_code):
    match = next ((entry for entry in councils_data if entry["census_code"] == council_code),None)
    if match:
        bbox_dict = match["bbox"]
        bbox_string = f"{bbox_dict['minx']},{bbox_dict['miny']},{bbox_dict['maxx']},{bbox_dict['maxy']}"
        return bbox_string
    else:
        return False
    
def get_formatted_bbox_for_council_code(council_code):
    match = next ((entry for entry in councils_data if entry["census_code"] == council_code),None)
    if match:
        bbox_dict = match["bbox"]
        bbox_values = (bbox_dict['minx'], bbox_dict['miny'], bbox_dict['maxx'], bbox_dict['maxy'])
        return bbox_values
    else:
        return False

def filter_properties_by_council_code(council_code, properties):
    if not council_code:
        return []

    uprn_to_council_dict = load_uprn_to_council(council_code)
    return [
        prop for prop in properties
        if uprn_to_council_dict.get(str(prop.uprn)) == council_code
    ]

def get_polygon_for_council_code(council_code):

    council_data = next(c for c in councils_data if c["census_code"] == council_code)
    
    geom = shape(council_data["geometry"])
    polygon = geom.geoms[0]
    original_coords = list(polygon.exterior.coords)
    latlon_coords = [[lat,lon]for lon, lat in original_coords]
    if latlon_coords[0] != latlon_coords[-1]:
        latlon_coords.append(latlon_coords[0])

    request_body = {
            "type": "Polygon",
            "coordinates": [latlon_coords]
        }
    return request_body

def _create_councils_data():
    gdf = gpd.read_file("data/bdline_gpkg_gb/Data/bdline_gb.gpkg", layer = "district_borough_unitary")

    #convert coordinates to correct format
    gdf = gdf.to_crs("EPSG:4326")
    target_council_codes = {"E07000207","E07000116","E07000085","E06000023"}
    gdf = gdf[gdf["Census_Code"].isin(target_council_codes)]

    councils_data = []
    for _, row in gdf.iterrows():
          
        name = row["Name"]
        census_code = row["Census_Code"]
        bounds = row.geometry.bounds
        bbox = {
                "minx": bounds[0],
                "miny": bounds[1],
                "maxx": bounds[2],
                "maxy": bounds[3]
        }
        geometry = row.geometry.__geo_interface__

        councils_data.append({
            "name": name,
            "census_code": census_code,
            "bbox": bbox,
            "geometry": geometry
        })
    
    with open("data/councils_bbox_data_DEMO.json", "w") as f:
        json.dump(councils_data, f, indent=2)

def _create_uprn_council_data():
     
    data = pd.read_csv("data/ONSUD_NOV_2025_SW.csv",
                        usecols=["UPRN", "LAD25CD"],
                        dtype={"UPRN": str}
    )
    data = data.rename(columns={"LAD25CD": "COUNCIL_CODE"})
    data.to_csv("data/uprn_to_council_SW.csv", index=False)