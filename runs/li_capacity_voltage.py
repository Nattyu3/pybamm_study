import pybamm

from pybamm_study.capacity import (
    estimate_active_material_mass_g,
    split_discharge_charge,
    to_specific_capacity_mAh_g,
)
from pybamm_study.outputs import save_capacity_voltage_result
from pybamm_study.paths import make_output_dir
from pybamm_study.solution import extract_basic_solution


# 見かけの比容量スケール [mAh/g]
# Chen2020 のセル容量をこの値で割って、仮想的な活物質質量を決める。
# 例: 5 Ah セルなら 5000 mAh / 170 mAh/g ≒ 29.4 g
TARGET_SPECIFIC_CAPACITY_MAH_G = 170.0

# 電圧窓 [V]
LOWER_CUTOFF_V = 2.5
UPPER_CUTOFF_V = 4.2
C_RATE = "C/5"


def main():
    out_dir = make_output_dir("li_capacity_voltage")

    model = pybamm.lithium_ion.SPM()
    parameter_values = pybamm.ParameterValues("Chen2020")

    active_material_mass_g, nominal_capacity_ah = estimate_active_material_mass_g(
        parameter_values,
        TARGET_SPECIFIC_CAPACITY_MAH_G,
    )

    experiment = pybamm.Experiment(
        [
            f"Discharge at {C_RATE} until {LOWER_CUTOFF_V} V",
            "Rest for 10 minutes",
            f"Charge at {C_RATE} until {UPPER_CUTOFF_V} V",
            f"Hold at {UPPER_CUTOFF_V} V until C/50",
            "Rest for 10 minutes",
        ]
    )

    sim = pybamm.Simulation(
        model,
        parameter_values=parameter_values,
        experiment=experiment,
    )
    solution = sim.solve()

    data, variable_names = extract_basic_solution(solution)

    branches = split_discharge_charge(
        voltage_v=data["voltage_v"],
        current_a=data["current_a"],
        capacity_ah=data["capacity_ah"],
    )

    discharge_specific_capacity = to_specific_capacity_mAh_g(
        branches["discharge_capacity_ah"],
        active_material_mass_g,
    )

    charge_specific_capacity = to_specific_capacity_mAh_g(
        branches["charge_capacity_ah"],
        active_material_mass_g,
    )

    saved_paths = save_capacity_voltage_result(
        out_dir=out_dir,
        prefix="li",
        data=data,
        branches=branches,
        discharge_specific_capacity=discharge_specific_capacity,
        charge_specific_capacity=charge_specific_capacity,
        info_lines=[
            "Li-ion PyBaMM capacity-voltage simulation",
            "model = lithium_ion.SPM",
            "parameter_values = Chen2020",
            (
                f"experiment = discharge at {C_RATE} to {LOWER_CUTOFF_V} V, "
                f"charge at {C_RATE} to {UPPER_CUTOFF_V} V, "
                "CV hold to C/50"
            ),
            f"nominal_capacity_Ah = {nominal_capacity_ah}",
            f"target_specific_capacity_mAh_g = {TARGET_SPECIFIC_CAPACITY_MAH_G}",
            f"estimated_active_material_mass_g = {active_material_mass_g}",
            f"time variable = {variable_names['time']}",
            f"voltage variable = {variable_names['voltage']}",
            f"capacity variable = {variable_names['capacity']}",
            f"current variable = {variable_names['current']}",
        ],
        plot_title="Li-ion charge/discharge simulation",
        ylim=(2.0, 4.4),
    )

    for path in saved_paths.values():
        print(f"saved: {path}")


if __name__ == "__main__":
    main()
