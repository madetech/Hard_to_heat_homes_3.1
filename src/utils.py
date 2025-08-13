from src.property import Property
from src.epc_api import epc_api_call, epc_api_call_address
from src.variables import EPC_TOKEN
from src.os_api import os_places_api_call

def get_properties_from_os(list_of_buildings):
    list_of_properties = []
    for i in range(len(list_of_buildings)):
        coordinates = list_of_buildings[i]["geometry"]["coordinates"][0][0]
        building = list_of_buildings[i]["properties"]
        uprn_array = building["uprnreference"]
        for j in range(len(uprn_array)):
            age = (
                "buildingage_year"
                if building["buildingage_year"]
                else "buildingage_period"
            )
            new_prop = Property(uprn_array[j]["uprn"])
            new_prop.connectivity = building["connectivity"]
            new_prop.age = building[age]
            new_prop.material = building["constructionmaterial"]
            new_prop.long = coordinates[0]
            new_prop.lat = coordinates[1]
            new_prop.building_id = building["sitereference"][0]["buildingid"]
            new_prop.roof_shape = building["roofshapeaspect_shape"]
            new_prop.roof_pitched_area = building['roofshapeaspect_areapitched_m2']
            new_prop.roof_southeast_area = building["roofshapeaspect_areafacingsoutheast_m2"]
            new_prop.roof_solar_panel_presence = building["roofmaterial_solarpanelpresence"]
            new_prop.roof_material = building["roofmaterial_primarymaterial"]
            list_of_properties.append(new_prop)

    return list_of_properties


def get_attributes_from_epc(prop, uprn):
    epc_params = format_urpn_from_property(uprn)
    epc_result = epc_api_call(
        {"Accept": "application/json", "Authorization": f"Basic {EPC_TOKEN}"}, epc_params
    )
    if epc_result:
        epc_data_by_uprn = {row["uprn"]: row for row in epc_result["rows"]}
        row = epc_data_by_uprn.get(str(prop.uprn))
        prop.epc_rating = row["current-energy-rating"]
        prop.epc_score = row["current-energy-efficiency"]
        prop.energy_usage = row["energy-consumption-current"]

def format_urpn_from_property(uprn):
    return f"uprn={uprn}"

def set_missing_addresses(property):
    if not property.address:
        response = os_places_api_call(property.uprn)
        if response:
            property.address = response['results'][0]['DPA']['ADDRESS']

def setting_void_properties(list_of_properties):
    for i in range(len(list_of_properties)):
        if i %3 == 0:
            list_of_properties[i].void = True

def filter_for_void(list_of_properties):

    void_properties = []

    for i in range(len(list_of_properties)):
        if list_of_properties[i].void == True:
            void_properties.append(list_of_properties[i])

    return void_properties

def get_addresses(properties):
    uprns = [p.uprn for p in properties]
    
    uprn_to_address = {}
    batch_size = 50
    for i in range(0, len(uprns), batch_size):
        batch = uprns[i:i+batch_size]
        params = [("uprn",u) for u in batch]
        response = epc_api_call_address(params)  

        if not response:
            break
        
        uprn_to_address_batch = {row["uprn"]: 
                                 f"{row["address"]}, {row["county"]}, {row['postcode']}"
                                 for row in response["rows"]}
                                 
        uprn_to_address.update(uprn_to_address_batch)

    for p in properties:
        if str(p.uprn) in uprn_to_address:
            p.address = uprn_to_address[str(p.uprn)]

    return properties