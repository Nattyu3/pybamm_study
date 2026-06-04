import pybamm

def main():
    print("PyBaMM version:", pybamm.__version__)

    model = pybamm.lithium_ion.SPM()
    simulation = pybamm.Simulation(model)

    solution = simulation.solve([0, 3600])

    voltage = solution["Terminal voltage [V]"](solution.t[-1])
    print(f"Voltage at final time: {voltage:.3f} V")

if __name__ == "__main__":
    main()
