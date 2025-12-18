MINIMUM_EPC_RATING = "D"
MINIMUM_FAILING_AGE = 1959
COLD_CONNECTIVITY = "Standalone"
WARM_MATERIALS = ["Brick Or Block Or Stone", "Contrete"]

class Property():
    def __init__(self, uprn):
        self.uprn = uprn
        self.owner_name = 'Unknown'
        self.owner_type = 'Unknown'
        self.company_reg_number = 'Unknown'
        self.epc_rating = 'No Rating Found'
        self.epc_score = 'No Score Found'
        self.address = ''
        self.age = 0
        self.connectivity = ''
        self.material = ''
        self.score = 0
        self.void = False
        self.long = 0
        self.lat = 0
        self.building_id = ''
        self.roof_shape = ""
        self.roof_pitched_area_m2 = 0
        self.roof_southeast_area_m2 = 0
        self.roof_solar_panel_presence = ''
        self.roof_material = ''
        self.energy_usage = 'No Usage Found'   
        self.height_relative_roof_base_m = 0
        self.green_roof_presence = ''

    def calculate_score(self):
        score = 0
        self.handle_age_string()
        if self.connectivity == COLD_CONNECTIVITY:
            score += 1
        if self.material not in WARM_MATERIALS and self.material != "":
            score += 1
        if self.epc_rating > MINIMUM_EPC_RATING or self.epc_rating == "":
            score += 1
        if self.age <= MINIMUM_FAILING_AGE and self.age > 0:
            score += 1

        self.score = score
        return score
    
    def handle_age_string(self):
        if self.age is None:
            self.age = MINIMUM_FAILING_AGE

        if self.age == "Unknown":
            self.age = MINIMUM_FAILING_AGE
            
        age_is_int = type(self.age) is int
        if not age_is_int:
            self.age = int(self.age[-4:])

    def set_owner_name(self, owner_name):
        self.owner_name = owner_name

    def set_owner_type(self, owner_type):
        self.owner_type = owner_type

    def set_company_registration_number(self, company_reg_num):
        self.company_reg_num = company_reg_num