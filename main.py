from frontend.boiler.boiler_console import BoilerConsole
from frontend.insulation.insulation_console import InsulationConsole
from frontend.joinery.joinery_console import JoineryConsole
from frontend.input_options import *
from frontend.io_dataclass import UserHomeInfo

def main():
	joinery_needed_savings: float = 0.0
	insulation_needed_savings: float = 0.0

	user_info: UserHomeInfo = generate_user_info()

	joinery_console = JoineryConsole(user_info)
	joinery_console.run()
	joinery_needed_savings = joinery_console.component.needed_energy_savings()

	insulation_console = InsulationConsole(user_info)
	insulation_console.run()
	insulation_needed_savings = insulation_console.component.needed_energy_savings()

	boiler_console = BoilerConsole(user_info, joinery_needed_savings, insulation_needed_savings)
	boiler_console.run()

def generate_user_info() -> UserHomeInfo:
	return 	UserHomeInfo(
				municipality			= Municipality.VOZDOVAC,
				construction_period		= ConstructionPeriod.PERIOD_1991_2012,
				dwelling_type			= DwellingType.APARTMENT,
				building_type			= BuildingType.HIGH_RISE,
				floor_area				= 60.0,
				height					= 2.7,
				heating_system_type		= HeatingSystemType.CENTRAL,
				heating_fuel_type		= HeatingFuelType.DISTRICT_HEATING,
				annual_fuel_consumption	= None,
				fuel_cost_per_unit		= 8,
				pipe_system_isolated 	= True
			)

if __name__ == "__main__":
	main()