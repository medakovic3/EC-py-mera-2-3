from frontend.io_dataclass import *

class Component:
    def __init__(self):
        self.output_data: OutputData = OutputData()
        self.user_house_info: UserHouseInfo = None
        self.insulation_info: InsulationInfo = None

    def calculate_output_data(
        self,
        user_house_info: UserHouseInfo,
        insulation_info: InsulationInfo
    ) -> OutputData:
        self.set_input_info(user_house_info, insulation_info)
        # TODO Get data from databse
        self.start_calculation()
        return self.output_data
    
    def set_input_info(
            self,
            user_house_info: UserHouseInfo,
            insulation_info: InsulationInfo
    ):
        self.user_house_info = user_house_info
        self.insulation_info = insulation_info

    def start_calculation(self):
        # TODO
        pass