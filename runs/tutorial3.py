# Basic plotting

import pybamm

model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model)
sim.solve([0, 3600])

(model.variable_names())

model.variables.search("electrolyte")

output_variables = ["Electrolyte concentration [mol.m-3]", "Voltage [V]"]
sim.plot(output_variables=output_variables)

output_variables = ["Voltage [V]"]
sim.plot(output_variables=output_variables)

sim.plot(
    [
        ["Electrode current density [A.m-2]", "Electrolyte current density [A.m-2]"],
        "Voltage [V]",
    ]
)

sim.plot_voltage_components()

sim.plot_voltage_components(split_by_electrode=True)

pybamm.print_citations()
