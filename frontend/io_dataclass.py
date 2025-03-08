from dataclasses import dataclass
from frontend.input_options import *
from typing import Optional

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
    annual_fuel_consumption: Optional[float]
    fuel_cost_per_unit: Optional[float]

@dataclass
class InsulationInfo:
    investment_cost: float
    insulated_construction_type: InsulatedConstructionType
    insulation_thickness: float
    insulated_area: float
    insulation_thermal_conductivity: float
