import os
import sys
from flask import Flask, render_template, request, redirect, url_for, session
from src.os_api import os_api_call
from src.utils import get_properties_from_os, get_attributes_from_epc, set_missing_addresses, setting_void_properties
from src.variables import OS_KEY
from src.council_data_utils import get_bbox_for_council_code, filter_properties_by_council_code
from src.generate_heat_map import generate_heat_map

app = Flask(__name__)

properties = []

app.secret_key = os.getenv("SESSION_SECRET_KEY")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        current_council_code = session.get("council_code")
        new_council_code = request.form.get("council")
        if current_council_code != new_council_code:
            session["council_code"] = new_council_code
            council_bbox = get_bbox_for_council_code(new_council_code)
            set_property_data(new_council_code, council_bbox)
        return redirect(url_for("home"))
    return render_template("login.html")

def set_property_data(council_code, council_bbox):
    HEADERS = {"Accept": "application/json"}
    PARAMS = {
        "key": OS_KEY,
        "filter": "buildinguse_oslandusetiera = 'Residential Accommodation' AND mainbuildingid_ismainbuilding = 'Yes'",
        "bbox": council_bbox,
        # "offset": 100,
         }
    
    global properties
    
    # links = os_api_call(HEADERS, PARAMS)["links"]
    # print(links[1]["href"])
    
    list_of_buildings = os_api_call(HEADERS, PARAMS, 0)["features"] + os_api_call(HEADERS, PARAMS, 100)["features"] + os_api_call(HEADERS, PARAMS, 200)["features"]
    
    print(len(list_of_buildings))
    print(list_of_buildings[0]["id"])
    sys.stdout.flush()
    
    properties = get_properties_from_os(list_of_buildings)
    properties = filter_properties_by_council_code(council_code, properties)
    properties = get_attributes_from_epc(properties)
    
    for i in range(len(properties)):
        properties[i].calculate_score()
    
    return

@app.route("/home")
def home():
   heat_map = generate_heat_map(session.get("council_code"))
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
