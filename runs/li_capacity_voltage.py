import pybamm

from pybamm_study.capacity import (
    estimate_active_material_mass_g,
    split_discharge_charge,
    to_specific_capacity_mAh_g,
)
from pybamm_study.outputs import (
    save_capacity_voltage_csv,
    save_info,
    save_raw_solution_csv,
)
from pybamm_study.paths import make_output_dir
from pybamm_study.plotting import plot_capacity_voltage
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

    raw_csv_path = out_dir / "li_raw_solution.csv"
    plot_csv_path = out_dir / "li_capacity_voltage.csv"
    png_path = out_dir / "li_capacity_voltage.png"
    info_path = out_dir / "li_info.txt"

    save_raw_solution_csv(
        raw_csv_path,
        time_s=data["time_s"],
        voltage_v=data["voltage_v"],
        current_a=data["current_a"],
        capacity_ah=data["capacity_ah"],
    )

    save_capacity_voltage_csv(
        plot_csv_path,
        discharge_specific_capacity=discharge_specific_capacity,
        discharge_voltage_v=branches["discharge_voltage_v"],
        charge_specific_capacity=charge_specific_capacity,
        charge_voltage_v=branches["charge_voltage_v"],
    )

    plot_capacity_voltage(
        png_path,
        discharge_specific_capacity=discharge_specific_capacity,
        discharge_voltage_v=branches["discharge_voltage_v"],
        charge_specific_capacity=charge_specific_capacity,
        charge_voltage_v=branches["charge_voltage_v"],
        title="Li-ion charge/discharge simulation",
        ylim=(2.0, 4.4),
    )

    save_info(
        info_path,
        [
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
            f"plot csv = {plot_csv_path.name}",
            f"raw csv = {raw_csv_path.name}",
            f"png = {png_path.name}",
        ],
    )

    print(f"saved: {plot_csv_path}")
    print(f"saved: {raw_csv_path}")
    print(f"saved: {png_path}")
    print(f"saved: {info_path}")


if __name__ == "__main__":
    main()
