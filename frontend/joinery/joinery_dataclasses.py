from dataclasses import dataclass
from frontend.input_options import *
from frontend.model.heating_fuel_parameters_model import HeatingFuelParameters

@dataclass
class JoineryInfo:
    investment_cost: float
    window_area: float
    window_airtightness: JoineryAirtightness
    window_material: JoineryMaterial
    window_glazing: WindowGlazingType
    window_U_new: float
    door_area: float
    door_material: JoineryMaterial
    door_U_new: float
    wind_exposure: WindExposure

@dataclass
class JoineryDBData:
    needed_energy_per_m2: float = 0.0
    hdd: float = 0.0
    heating_fuel: HeatingFuelParameters = None
    air_changes_per_hour: float = 0.0
    window_U_old: float = 0.0
    door_U_old: float = 0.0