from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pybamm


def make_output_dir() -> Path:
    project_root = Path(__file__).resolve().parents[1]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = project_root / "results" / timestamp
    out_dir.mkdir(parents=True, exist_ok=False)
    return out_dir


def main():
    out_dir = make_output_dir()

    model = pybamm.lithium_ion.SPM()
    simulation = pybamm.Simulation(model)
    solution = simulation.solve([0, 3600])

    time_minutes = solution["Time [s]"].entries / 60
    voltage = solution["Terminal voltage [V]"].entries

    png_path = out_dir / "spm_voltage.png"

    plt.figure()
    plt.plot(time_minutes, voltage)
    plt.xlabel("Time [min]")
    plt.ylabel("Terminal voltage [V]")
    plt.title("SPM discharge example")
    plt.grid(True)
    plt.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close()

    info_path = out_dir / "spm_info.txt"
    info_path.write_text(
        "SPM discharge example\n"
        "model = lithium_ion.SPM\n"
        "solve_time = [0, 3600] s\n"
        f"png = {png_path.name}\n"
    )

    print(f"Saved: {png_path}")
    print(f"Saved: {info_path}")


if __name__ == "__main__":
    main()