import geopandas as gpd
from pathlib import Path


input_file= Path("data/bristol_buildings.geojson")
output_file = Path("data/bristol_streets_grouped.geojson")


def group_buildings_by_street(in_path, out_path):
    if not Path(in_path).exists():
        print(f"Error: Could not find the file '{in_path}' in this folder.")
        return

    print(f"Reading {in_path}...")
    gdf = gpd.read_file(in_path)
    
    if 'addr:street' not in gdf.columns:
        print("Error: The column 'addr:street' was not found in the GeoJSON.")
        print(f"Available columns: {list(gdf.columns)}")
        return

    print(f"Merging {len(gdf)} buildings into street clusters...")
    
    street_clusters = gdf.dissolve(by='addr:street', as_index=False)
    
    print(f"Saving to {out_path}...")
    street_clusters.to_file(out_path, driver='GeoJSON')
    print("Success!")

if __name__ == "__main__":
    group_buildings_by_street(input_file, output_file)
