from frontend.boiler.boiler_console import BoilerConsole
from frontend.insulation.insulation_console import InsulationConsole
from frontend.joinery.joinery_console import JoineryConsole

joinery_console: JoineryConsole = None
insulation_console: InsulationConsole = None
boiler_console: BoilerConsole = None

def main():
	joinery_console = JoineryConsole()
	joinery_console.run()

	insulation_console = InsulationConsole()
	insulation_console.run()

	boiler_console = BoilerConsole()
	boiler_console.run()

if __name__ == "__main__":
	main()