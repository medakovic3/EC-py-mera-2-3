from typing import Optional
from frontend.io_dataclass import *

class Console:
	def __init__(self):
		self.output_data: Optional[OutputData] = None
		self.user_house_info: Optional[UserHouseInfo] = None
		self.insulation_info: Optional[InsulationInfo] = None

	def run(self):
		self.generate_input_data()
		# TODO Calculate output data
		self.print_output_data()

	def generate_input_data(self):
		# TODO
		None

	def print_output_data(self):
		# TODO
		None
