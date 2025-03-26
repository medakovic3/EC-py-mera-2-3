from dataclasses import dataclass
from frontend.input_options import *
from typing import Optional
from frontend.model.heating_fuel_parameters_model import HeatingFuelParameters
from frontend.model.insulated_surface_parameters_model import InsulatedSurfaceParameters

@dataclass
class OutputData:
    annual_cost_savings: float = 0.0
    payback_period: float = 0.0
    annual_final_energy_savings: float = 0.0
    co2_emission_reduction: float = 0.0

@dataclass
class UserHomeInfo:
    municipality: Municipality
    construction_period: ConstructionPeriod
    dwelling_type: DwellingType
    building_type: BuildingType
    floor_area: float
    height: Optional[float]
    heating_system_type: HeatingSystemType
    heating_fuel_type: HeatingFuelType
    annual_fuel_consumption: Optional[float]
    fuel_cost_per_unit: float
    pipe_system_isolated: bool

@dataclass
class InsulationInfo:
    investment_cost: float
    insulated_surface_type: InsulatedSurfaceType
    insulation_thickness: float
    insulated_area: float
    insulation_thermal_conductivity: float

@dataclass
class BoilerInfo:
    investment_cost: float
    new_heating_fuel_type: HeatingFuelType
    new_fuel_cost_per_unit: float
    new_fuel_efficiency: float
    pipe_system_change: bool
    thermostat_installation: bool
    
@dataclass
class InsulationDBData:
    needed_energy_per_m2: float = 0.0
    hdd: float = 0.0
    heating_fuel: HeatingFuelParameters = None
    insulated_surface: InsulatedSurfaceParameters = None

@dataclass
class BoilerDBData:
    needed_energy_per_m2: float = 0.0
    hdd: float = 0.0
    heating_fuel: HeatingFuelParameters = None
    new_heating_fuel: HeatingFuelParameters = None
