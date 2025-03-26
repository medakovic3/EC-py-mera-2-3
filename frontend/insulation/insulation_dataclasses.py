from dataclasses import dataclass
from frontend.input_options import *
from frontend.model.heating_fuel_parameters_model import HeatingFuelParameters
from frontend.model.insulated_surface_parameters_model import InsulatedSurfaceParameters

@dataclass
class InsulationInfo:
    investment_cost: float
    insulated_surface_type: InsulatedSurfaceType
    insulation_thickness: float
    insulated_area: float
    insulation_thermal_conductivity: float

@dataclass
class InsulationDBData:
    needed_energy_per_m2: float = 0.0
    hdd: float = 0.0
    heating_fuel: HeatingFuelParameters = None
    insulated_surface: InsulatedSurfaceParameters = None