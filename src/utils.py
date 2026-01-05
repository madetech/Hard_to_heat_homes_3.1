import pandas as pd
import re
from src.property import Property
from src.epc_api import epc_api_call_address
from src.variables import EPC_TOKEN


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
            new_prop.roof_pitched_area_m2 = building['roofshapeaspect_areapitched_m2']
            new_prop.roof_southeast_area_m2 = building["roofshapeaspect_areafacingsoutheast_m2"]
            new_prop.roof_solar_panel_presence = building["roofmaterial_solarpanelpresence"]
            new_prop.roof_material = building["roofmaterial_primarymaterial"]
            new_prop.height_relative_roof_base_m = building["height_relativeroofbase_m"]
            new_prop.green_roof_presence = building["roofmaterial_greenroofpresence"]
            list_of_properties.append(new_prop)

    return list_of_properties

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

def remove_blank_addresses(properties):
    filtered_addresses = []
    
    for prop in properties:
        if prop.address != "":
            filtered_addresses.append(prop)

    return filtered_addresses

def normalise_address(addr: str) -> str:
    addr = addr.lower()

    # removing county names to make matching more consistent
    counties = ["kent", "tunbridge wells", "surrey", "east hampshire", "hampshire", 'bristol']
    
    for c in counties:
        # \b is word boundary e.g \bkent\b matches 'kent' but not 'kentish'
        addr = re.sub(rf"\b{c}\b", "", addr)

    # ^ (not) \w (alphanumeric) or \s (whitespace) in [] (group of characters)
    # replace anything not alphanumeric or whitespace with ""
    addr = re.sub(r"[^\w\s]", "", addr)

    return " ".join(addr.split())

def match_property_to_ccod(csv_path: str, property: property):
    df = pd.read_csv(csv_path, low_memory=False)

    df["__normalised_address"] = df["Property Address"].astype(str).apply(normalise_address)

    target = normalise_address(str(property.address))

    match = df[df["__normalised_address"] == target]

    if match.empty:
        return 
    
    property.set_owner_name(str(match.iloc[0]["Proprietor Name (1)"]))
    property.set_owner_type(str(match.iloc[0]["Proprietorship Category (1)"]))
    property.set_company_registration_number(str(match.iloc[0]["Company Registration No. (1)"]))
    
    return