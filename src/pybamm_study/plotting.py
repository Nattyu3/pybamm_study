from pathlib import Path

import matplotlib.pyplot as plt


def plot_capacity_voltage(
    path: Path,
    discharge_specific_capacity,
    discharge_voltage_v,
    charge_specific_capacity,
    charge_voltage_v,
    title: str,
    xlim_left: float = 0,
    ylim: tuple[float, float] | None = None,
):
    """
    放電・充電の比容量-電圧曲線をPNG保存する。
    """
    plt.figure()

    if len(discharge_specific_capacity) > 0:
        plt.plot(
            discharge_specific_capacity,
            discharge_voltage_v,
            label="discharge",
        )

    if len(charge_specific_capacity) > 0:
        plt.plot(
            charge_specific_capacity,
            charge_voltage_v,
            label="charge",
        )

    plt.xlabel("Specific capacity [mAh/g]")
    plt.ylabel("Terminal voltage [V]")
    plt.title(title)
    plt.xlim(left=xlim_left)

    if ylim is not None:
        plt.ylim(*ylim)

    plt.grid(True)
    plt.legend()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
