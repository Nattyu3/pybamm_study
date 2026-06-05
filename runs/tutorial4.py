# Setting parameter values

import pybamm

parameter_values = pybamm.ParameterValues("Chen2020")

print(parameter_values)

parameter_values["Electrode height [m]"]

parameter_values.search("electrolyte")

model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model, parameter_values=parameter_values)
sim.solve([0, 3600])
sim.plot()

model.print_parameter_info()

parameter_values["Current function [A]"] = 10

sim = pybamm.Simulation(model, parameter_values=parameter_values)
sim.solve([0, 3600])
sim.plot()

import numpy as np


def my_current(t):
    return pybamm.sin(2 * np.pi * t / 60)


parameter_values["Current function [A]"] = my_current

sim = pybamm.Simulation(model, parameter_values=parameter_values)
t_eval = np.arange(0, 121, 1)
sim.solve(t_eval=t_eval)
sim.plot(["Current [A]", "Voltage [V]"])

import matplotlib.pyplot as plt

parameter_values["Current function [A]"] = "[input]"
sim = pybamm.Simulation(model, parameter_values=parameter_values)
solns = []
for c in [0.1, 0.2, 0.3]:
    soln = sim.solve([0, 3600], inputs={"Current function [A]": c})
    plt.plot(soln["Time [s]"].entries, soln["Voltage [V]"].entries, label=f"{c} A")
    solns.append(soln["Terminal voltage [V]"].entries)
plt.xlabel("Time [s]")
plt.ylabel("Terminal voltage [V]")
plt.legend()
plt.show()

def cube(t):
    return t**3


parameter_values = pybamm.ParameterValues(
    {
        "Negative electrode thickness [m]": 1e-4,
        "Positive electrode thickness [m]": 1.2e-4,
        "Current function [A]": cube,
    }
)

pybamm.print_citations()
