from frontend.boiler.boiler_dataclasses import BoilerInfo
from frontend.io_dataclass import *
from frontend.boiler.boiler_component import BoilerComponent

class BoilerConsole:
	def __init__(self, j_nd_save: float, i_nd_save: float):
		self.output_data: OutputData = None
		self.user_home_info: UserHomeInfo = None
		self.boiler_info: BoilerInfo = None
		self.component = BoilerComponent(j_nd_save, i_nd_save)

	def run(self):
		self.generate_input_data()
		self.output_data = self.component.calculate_output_data(
			self.user_home_info,
			self.boiler_info
		)
		self.print_output_data()

	def generate_input_data(self):
		self.user_home_info = UserHomeInfo(
			municipality			= Municipality.VOZDOVAC,
			construction_period		= ConstructionPeriod.PERIOD_1991_2012,
			dwelling_type			= DwellingType.APARTMENT,
			building_type			= BuildingType.HIGH_RISE,
			floor_area				= 60.0,
			height					= None,
			heating_system_type		= HeatingSystemType.CENTRAL,
			heating_fuel_type		= HeatingFuelType.DISTRICT_HEATING,
			annual_fuel_consumption	= None,
			fuel_cost_per_unit		= 8,
			pipe_system_isolated	= True
		)

		self.boiler_info = BoilerInfo(
			investment_cost = 300000,
			new_heating_fuel_type = HeatingFuelType.PELLET,
			new_fuel_cost_per_unit = 33000,
			new_fuel_efficiency = 0.85,
			pipe_system_change = True,
			thermostat_installation = False
		)

	def print_output_data(self):
		fin_en_savings = self.output_data.annual_final_energy_savings
		cost_savings = self.output_data.cost_savings
		payback_period = self.output_data.payback_period
		co2_emission_red = self.output_data.co2_emission_reduction

		print("Boiler output:")
		print(f"	Annual final energy savings: {fin_en_savings:10.0f} kWh")
		print(f"	Annual cost savings:         {cost_savings:10.0f} rsd")
		print(f"	Payback period:              {payback_period:10.1f} years")
		print(f"	CO2 emission reduction:      {co2_emission_red:10.1f} kg/kWh")
