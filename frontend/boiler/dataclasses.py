from dataclasses import dataclass
from frontend.input_options import HeatingFuelType
from frontend.model.heating_fuel_parameters_model import HeatingFuelParameters

@dataclass
class BoilerInfo:
    investment_cost: float
    new_heating_fuel_type: HeatingFuelType
    new_fuel_cost_per_unit: float
    new_fuel_efficiency: float
    pipe_system_change: bool
    thermostat_installation: bool

@dataclass
class BoilerDBData:
    needed_energy_per_m2: float = 0.0
    hdd: float = 0.0
    heating_fuel: HeatingFuelParameters = None
    new_heating_fuel: HeatingFuelParameters = None