import os
from flask import Flask, render_template, request, redirect, url_for, session
from src.utils import get_properties_from_os, get_attributes_from_epc, remove_blank_addresses, match_property_to_ccod
from src.variables import OS_KEY
from src.council_data_utils import get_bbox_for_council_code, filter_properties_by_council_code
from src.generate_heat_map import generate_heat_map
from src.building_collection import BuildingCollection

app = Flask(__name__)

properties = []

app.secret_key = os.getenv("SESSION_SECRET_KEY")

@app.route("/")
def login():
    council_code = "E06000023"
    council_bbox = get_bbox_for_council_code(council_code)
    return set_property_data(council_code, council_bbox)


def set_property_data(council_code, council_bbox):
    
    list_of_buildings = BuildingCollection(council_bbox, 3).produce_list()
    
    global properties
    properties = get_properties_from_os(list_of_buildings)
    properties = filter_properties_by_council_code(council_code, properties)
    properties = get_attributes_from_epc(properties)
    properties = remove_blank_addresses(properties)

    for i in range(len(properties)):
        properties[i].calculate_score()

    target_csv_path = 'data/TEST_BRISTOL_CCOD_DEC_2025.csv'
    
    for prop in properties:
        match_property_to_ccod(target_csv_path, prop)
    
    heat_map = generate_heat_map(council_code)
    return render_template("home.html", properties=properties, key=OS_KEY, heat_map=heat_map)

@app.route("/<int:uprn>")
def property(uprn):
    
    prop = None
    for property in properties:
        if property.uprn == uprn:
            prop = property 
            break
        
    return render_template("property.html", property=prop, key=OS_KEY)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
