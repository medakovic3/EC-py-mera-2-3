from frontend.boiler.boiler_console import BoilerConsole
from frontend.insulation.insulation_console import InsulationConsole
from frontend.joinery.joinery_console import JoineryConsole

joinery_needed_savings: float = 0.0
insulation_needed_savings: float = 0.0

def main():
	joinery_console = JoineryConsole()
	joinery_console.run()
	joinery_needed_savings = joinery_console.component.needed_energy_savings()

	insulation_console = InsulationConsole()
	insulation_console.run()
	insulation_needed_savings = insulation_console.component.needed_energy_savings()

	boiler_console = BoilerConsole(joinery_needed_savings, insulation_needed_savings)
	boiler_console.run()

if __name__ == "__main__":
	main()