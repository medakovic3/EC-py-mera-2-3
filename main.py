from frontend.boiler.boiler_console import BoilerConsole
from frontend.insulation.insulation_console import InsulationConsole
from frontend.joinery.joinery_console import JoineryConsole

def main():
	console = JoineryConsole()
	# console = InsulationConsole()
	# console = BoilerConsole()
	console.run()

if __name__ == "__main__":
	main()