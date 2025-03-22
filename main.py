from frontend.boiler.boiler_console import BoilerConsole
from frontend.insulation.insulation_console import InsulationConsole

def main():
	# console = InsulationConsole()
	console = BoilerConsole()
	console.run()

if __name__ == "__main__":
	main()