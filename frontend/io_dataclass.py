from dataclasses import dataclass

@dataclass
class OutputData:
    annual_cost_savings: float
    payback_period: float
    annual_final_energy_savings: float
    co2_emission_reduction: float