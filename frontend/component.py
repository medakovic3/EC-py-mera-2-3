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
        self.user_home_info: UserHomeInfo = None
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
        user_house_info: UserHomeInfo,
        insulation_info: InsulationInfo
    ) -> OutputData:
        self.set_input_info(user_house_info, insulation_info)
        self.load_db_data()
        self.start_calculation()
        return self.output_data
    
    def set_input_info(
            self,
            user_house_info: UserHomeInfo,
            insulation_info: InsulationInfo
    ):
        self.user_home_info = user_house_info
        self.insulation_info = insulation_info

    def load_db_data(self):
        self.load_hdd()
        self.load_needed_energy()
        self.load_insulated_surface_parameters()
        self.load_heating_fuel_parameters()

    def load_hdd(self):
        municipality_name = self.user_home_info.municipality.value
        self.hdd = self.municipality_service.get_hdd_by_municipality(municipality_name)

    def load_needed_energy(self):
        construction_period = self.user_home_info.construction_period.value
        dwelling_type = self.user_home_info.dwelling_type
        dwelling_type_str = dwelling_type.value

        if dwelling_type == DwellingType.APARTMENT:
            building_type_str = self.user_home_info.building_type.value
            dwelling_type_str += " " + building_type_str
        
        self.needed_energy_per_m2 = self.needed_energy_service.get_needed(
                                        construction_period,
                                        dwelling_type_str
                                    )       

    def load_insulated_surface_parameters(self):
        insulated_surface_type = self.insulation_info.insulated_surface_type.value
        construction_period = self.user_home_info.construction_period.value
        self.insulated_surface = \
            self.insulated_surface_service.get_insulated_surface_parameters(
                insulated_surface_type, construction_period
            )

    def load_heating_fuel_parameters(self):
        heating_fuel_type = self.user_home_info.heating_fuel_type.value
        heating_system_type = self.user_home_info.heating_system_type.value
        self.heating_fuel = self.heating_fuel_service.get_heating_fuel_parameters(
            heating_fuel_type,
            heating_system_type
        )

    def start_calculation(self):
        investment_cost: float = self.insulation_info.investment_cost
        self.output_data.payback_period = \
                            investment_cost / self.annual_cost_savings()
        
    def annual_cost_savings(self) -> float:
        self.output_data.annual_cost_savings = \
            self.annual_final_energy_savings() * \
            self.heating_fuel.consumption_per_kWh * \
            self.user_home_info.fuel_cost_per_unit
        return self.output_data.annual_cost_savings
    
    def annual_final_energy_savings(self):
        self.output_data.annual_final_energy_savings = \
            self.needed_energy_savings() / \
            self.efficiency() * \
            self.real_consumption_coef()
        return self.output_data.annual_final_energy_savings

    def efficiency(self):
        return  self.heating_fuel.efficiency.heating_fuel * \
                self.heating_fuel.efficiency.pipe_system * \
                self.heating_fuel.efficiency.pipe_regulation

    def needed_energy_savings(self):
        return  0.85 * self.insulated_surface.fxi * \
                self.insulation_info.insulated_area * \
                (self.insulated_surface.U - self.U_new()) * self.hdd * 24 / 1000
    
    def U_new(self):
        return 1 / self.R_new()
    
    def R_new(self):
        return  self.R_existing() + self.insulation_info.insulation_thickness / \
                self.insulation_info.insulation_thermal_conductivity

    def R_existing(self):
        return 1 / self.insulated_surface.U
    
    def real_consumption_coef(self):
        return self.real_fuel_consumption() / self.calculated_fuel_consumption()
    
    def real_fuel_consumption(self):
        return  self.user_home_info.annual_fuel_consumption if \
                self.user_home_info.annual_fuel_consumption else \
                self.calculated_fuel_consumption()
    
    def calculated_fuel_consumption(self):
        return self.final_energy() / self.heating_fuel.consumption_per_kWh
    
    def final_energy(self):
        return self.needed_energy() / self.efficiency()
    
    def needed_energy(self):
        return self.needed_energy_per_m2 * self.hdd / 2665.56 * \
                                                self.user_home_info.floor_area
