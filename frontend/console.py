from typing import Optional
from io_dataclass import *

class Console:
	def __init__(self):
		self.output_data: Optional[OutputData] = None
		self.user_house_info: Optional[UserHouseInfo] = None
		self.insulation_info: Optional[InsulationInfo] = None
