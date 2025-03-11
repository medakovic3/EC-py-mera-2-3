from typing import Optional
from frontend.io_dataclass import *
from frontend.component import Component

class Console:
	def __init__(self):
		self.output_data: OutputData = None
		self.user_house_info: UserHouseInfo = None
		self.insulation_info: InsulationInfo = None
		self.component = Component()

	def run(self):
		self.generate_input_data()
		self.output_data = self.component.calculate_output_data(
			self.user_house_info,
			self.insulation_info
		)
		self.print_output_data()

	def generate_input_data(self):
		self.user_house_info = UserHouseInfo(
			municipality			= Municipality.VOZDOVAC,
			construction_period		= ConstructionPeriod.PERIOD_1991_2012,
			dwelling_type			= DwellingType.APARTMENT,
			building_type			= BuildingType.HIGH_RISE,
			floor_area				= 60.0,
			heating_system_type		= HeatingSystemType.CENTRAL,
			heating_fuel_type		= HeatingFuelType.DISTRICT_HEATING,
			annual_fuel_consumption	= None,
			fuel_cost_per_unit		= None
		)

		self.insulation_info = InsulationInfo(
			investment_cost					= 300000.0,
			insulated_surface_type			= InsulatedSurfaceType.EXTERNAL_WALL,
			insulation_thickness			= 15.0,
			insulated_area					= 30.0,
			insulation_thermal_conductivity	= 0.035
		)

	def print_output_data(self):
		# TODO
		None
