from frontend.io_dataclass import *
from frontend.model.heating_fuel_parameters_model import HeatingFuelParameters
from frontend.model.insulated_surface_parameters_model import InsulatedSurfaceParameters
from frontend.service.municipality_service import MunicipalityService

class Component:
    def __init__(self):
        self.output_data: OutputData = OutputData()
        self.user_house_info: UserHouseInfo = None
        self.insulation_info: InsulationInfo = None

        self.needed_energy_per_m2: float = 0.0
        self.hdd: float = 0.0
        self.heating_fuel: HeatingFuelParameters = None
        self.insulated_surface: InsulatedSurfaceParameters = None

        self.municipality_service = MunicipalityService()

    def calculate_output_data(
        self,
        user_house_info: UserHouseInfo,
        insulation_info: InsulationInfo
    ) -> OutputData:
        self.set_input_info(user_house_info, insulation_info)
        self.load_db_data()
        self.start_calculation()
        return self.output_data
    
    def set_input_info(
            self,
            user_house_info: UserHouseInfo,
            insulation_info: InsulationInfo
    ):
        self.user_house_info = user_house_info
        self.insulation_info = insulation_info

    def load_db_data(self):
        municipality_name = self.user_house_info.municipality.value
        self.hdd = self.municipality_service.get_hdd_by_municipality(municipality_name)

    def start_calculation(self):
        # TODO
        pass