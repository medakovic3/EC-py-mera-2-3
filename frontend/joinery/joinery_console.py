from frontend.io_dataclass import *
from frontend.joinery.joinery_dataclasses import JoineryInfo
from frontend.joinery.joinery_component import JoineryComponent

class JoineryConsole:
	def __init__(self, user_info: UserHomeInfo):
		self.output_data: OutputData = None
		self.user_home_info: UserHomeInfo = user_info
		self.joinery_info: JoineryInfo = None
		self.component = JoineryComponent()

	def run(self):
		self.generate_input_data()
		self.output_data = self.component.calculate_output_data(
			self.user_home_info,
			self.joinery_info
		)
		self.print_output_data()

	def generate_input_data(self):
		self.joinery_info = JoineryInfo(
			investment_cost = 300000,
			window_area = 15,
			window_airtightness = JoineryAirtightness.MODERATE,
			window_material = JoineryMaterial.WOOD,
			window_glazing = WindowGlazingType.SINGLE_GLAZING,
			window_U_new = 1.2,
			door_area = 2,
			door_material = JoineryMaterial.WOOD,
			door_U_new = 1.5,
			wind_exposure = WindExposure.MODERATELY_SHELTERED
		)

	def print_output_data(self):
		fin_en_savings = self.output_data.final_energy_savings
		cost_savings = self.output_data.cost_savings
		payback_period = self.output_data.payback_period
		co2_emission_red = self.output_data.co2_emission_reduction

		print("Joinery output:")
		print(f"	Annual final energy savings: {fin_en_savings:10.0f} kWh")
		print(f"	Annual cost savings:         {cost_savings:10.0f} rsd")
		print(f"	Payback period:              {payback_period:10.1f} years")
		print(f"	CO2 emission reduction:      {co2_emission_red:10.1f} kg/kWh")
