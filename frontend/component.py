from frontend.io_dataclass import *
from frontend.model.heating_fuel_parameters_model import HeatingFuelParameters
from frontend.model.insulated_surface_parameters_model import InsulatedSurfaceParameters
from frontend.service.heating_fuel_service import HeatingFuelService
from frontend.service.municipality_service import MunicipalityService
from frontend.service.needed_energy_service import NeededEnergyService
from frontend.service.insulated_surface_service import InsulatedSurfaceService

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
        self.needed_energy_service = NeededEnergyService()
        self.insulated_surface_service = InsulatedSurfaceService()
        self.heating_fuel_service = HeatingFuelService()

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
        self.load_hdd()
        self.load_needed_energy()
        self.load_insulated_surface_parameters()
        self.load_heating_fuel_parameters()

    def load_hdd(self):
        municipality_name = self.user_house_info.municipality.value
        self.hdd = self.municipality_service.get_hdd_by_municipality(municipality_name)

    def load_needed_energy(self):
        construction_period = self.user_house_info.construction_period.value
        dwelling_type = self.user_house_info.dwelling_type
        dwelling_type_str = dwelling_type.value
        if dwelling_type == DwellingType.APARTMENT:
            building_type_str = self.user_house_info.building_type.value
            dwelling_type_str += " " + building_type_str
        self.needed_energy_per_m2 = self.needed_energy_service.get_needed(
                                        construction_period,
                                        dwelling_type_str
                                    )       

    def load_insulated_surface_parameters(self):
        insulated_surface_type = self.insulation_info.insulated_surface_type.value
        construction_period = self.user_house_info.construction_period.value
        self.insulated_surface = \
            self.insulated_surface_service.get_insulated_surface_parameters(
                insulated_surface_type, construction_period
            )

    def load_heating_fuel_parameters(self):
        heating_fuel_type = self.user_house_info.heating_fuel_type.value
        heating_system_type = self.user_house_info.heating_system_type.value
        self.heating_fuel = self.heating_fuel_service.get_heating_fuel_parameters(
            heating_fuel_type,
            heating_system_type
        )

    def start_calculation(self):
        # TODO
        pass