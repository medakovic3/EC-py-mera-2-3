from dataclasses import dataclass

@dataclass
class Efficiency:
    heating_fuel: float
    pipe_system: float
    pipe_regulation: float


@dataclass
class HeatingFuelParameters:
    efficiency: Efficiency
    consumption_per_kWh: float
    prim_en_conv_factor: float
    co2_emission: float
