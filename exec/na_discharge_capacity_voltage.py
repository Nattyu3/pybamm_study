from datetime import datetime
from pathlib import Path
import csv

import matplotlib.pyplot as plt
import pybamm


ACTIVE_MATERIAL_MASS_G = 0.020  # 仮に20 mg


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def make_output_dir() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = project_root() / "results" / timestamp
    out_dir.mkdir(parents=True, exist_ok=False)
    return out_dir


def get_entries(solution, candidates):
    """PyBaMMの変数名ゆれに対応して、最初に見つかった変数を返す。"""
    for name in candidates:
        try:
            return solution[name].entries, name
        except KeyError:
            pass
    raise KeyError(f"None of these variables were found: {candidates}")


def main():
    out_dir = make_output_dir()

    # Sodium-ion DFN
    model = pybamm.sodium_ion.BasicDFN()

    # まずは単純な放電
    # 公式例に近い形で C_rate を使う
    c_rate = 1 / 12

    sim = pybamm.Simulation(model, C_rate=c_rate)
    solution = sim.solve([0, 4000 / c_rate])

    time_s, time_name = get_entries(solution, ["Time [s]"])
    voltage_v, voltage_name = get_entries(
        solution,
        ["Voltage [V]", "Terminal voltage [V]"],
    )
    capacity_ah, capacity_name = get_entries(solution, ["Discharge capacity [A.h]"])

    # Ah -> mAh, さらに g で割る
    specific_capacity_mAh_g = capacity_ah * 1000.0 / ACTIVE_MATERIAL_MASS_G

    # CSV保存
    csv_path = out_dir / "na_discharge_capacity_voltage.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_s", "specific_capacity_mAh_g", "voltage_V"])
        for t, q, v in zip(time_s, specific_capacity_mAh_g, voltage_v):
            writer.writerow([t, q, v])

    # プロット保存
    png_path = out_dir / "na_discharge_capacity_voltage.png"
    plt.figure()
    plt.plot(specific_capacity_mAh_g, voltage_v)
    plt.xlabel("Specific capacity [mAh/g]")
    plt.ylabel("Voltage [V]")
    plt.title("Na-ion discharge simulation")
    plt.grid(True)
    plt.savefig(png_path, dpi=200, bbox_inches="tight")
    plt.close()

    # メタ情報
    info_path = out_dir / "na_info.txt"
    info_path.write_text(
        "\n".join(
            [
                "Na-ion PyBaMM discharge simulation",
                "model = sodium_ion.BasicDFN",
                f"C_rate = {c_rate}",
                f"active_material_mass_g = {ACTIVE_MATERIAL_MASS_G}",
                f"time variable = {time_name}",
                f"voltage variable = {voltage_name}",
                f"capacity variable = {capacity_name}",
                f"csv = {csv_path.name}",
                f"png = {png_path.name}",
            ]
        )
        + "\n"
    )

    print(f"saved: {csv_path}")
    print(f"saved: {png_path}")
    print(f"saved: {info_path}")


if __name__ == "__main__":
    main()
