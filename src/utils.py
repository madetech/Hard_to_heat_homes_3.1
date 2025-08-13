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

def get_attributes_from_epc(properties):
    uprns = [p.uprn for p in properties]
    
    uprn_to_epc_data = {}
    batch_size = 50
    for i in range(0, len(uprns), batch_size):
        batch = uprns[i:i+batch_size]
        params = [("uprn",u) for u in batch]
        response = epc_api_call_address(params)  

        if not response:
            break
        
        uprn_to_address_batch = {row["uprn"]: 
                                {
                                "address": f"{row["address"]}, {row["county"]}, {row['postcode']}",
                                "rating": f"{row["current-energy-rating"]}",
                                "score": f"{row["current-energy-efficiency"]}",
                                "consumption": f"{row["energy-consumption-current"]}"
                                }
                                 for row in response["rows"]}
                               
        uprn_to_epc_data.update(uprn_to_address_batch)

    for p in properties:
        if str(p.uprn) in uprn_to_epc_data:
            p.address = uprn_to_epc_data[str(p.uprn)]["address"]
            p.epc_rating = uprn_to_epc_data[str(p.uprn)]["rating"]
            p.epc_score = uprn_to_epc_data[str(p.uprn)]["score"]
            p.energy_usage = uprn_to_epc_data[str(p.uprn)]["consumption"]

    return properties