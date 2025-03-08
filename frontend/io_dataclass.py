from dataclasses import dataclass
from input_options import *

@dataclass
class OutputData:
    annual_cost_savings: float
    payback_period: float
    annual_final_energy_savings: float
    co2_emission_reduction: float

@dataclass
class UserHouseInfo:
    municipality: Municipality
    construction_period: ConstructionPeriod
    dwelling_type: DwellingType
    building_type: BuildingType
    floor_area: float
    heating_system_type: HeatingSystemType
    heating_fuel_type: HeatingFuelType
    annual_fuel_consumption: float
    fuel_cost_per_unit: float