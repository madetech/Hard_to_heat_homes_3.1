import geopandas as gpd
import pandas as pd
import json
from shapely.geometry import shape
from src.epc_api import epc_api_call_address

with open("data/councils_data_DEMO.json") as bbox_json:
        councils_data = json.load(bbox_json)
df = pd.read_csv("data/uprn_to_council_data_SE_DEMO.csv", dtype={"UPRN": str, "COUNCIL_CODE": str})

#use dictionary for speed
uprn_to_council_dict = pd.Series(df.COUNCIL_CODE.values, index=df.UPRN).to_dict()

def _create_councils_data():
    gdf = gpd.read_file("data/bdline_gpkg_gb/Data/bdline_gb.gpkg", layer = "district_borough_unitary")

    #convert coordinates to correct format
    gdf = gdf.to_crs("EPSG:4326")
    target_council_codes = {"E07000207","E07000116","E07000085"}
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

def get_bbox_for_council_code(council_code):
    match = next ((entry for entry in councils_data if entry["census_code"] == council_code),None)
    if match:
        bbox_dict = match["bbox"]
        bbox_string = f"{bbox_dict['minx']},{bbox_dict['miny']},{bbox_dict['maxx']},{bbox_dict['maxy']}"
        return bbox_string
    else:
        return False

def _create_uprn_council_data():
     
    data = pd.read_csv("data/onsud_apr_2025/ONSUD_APR_2025_SE.csv",
                        usecols=["UPRN", "LAD24CD"],
                        dtype={"UPRN": str}
    )
    data = data.rename(columns={"LAD24CD": "COUNCIL_CODE"})
    data.to_csv("data/uprn_to_council_SE.csv", index=False)

def get_council_code_for_uprn(uprn):
    return uprn_to_council_dict.get(uprn)

def filter_properties_by_council_code(council_code, properties):
    return list(filter(lambda x: get_council_code_for_uprn(str(x.uprn)) == council_code, properties))

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