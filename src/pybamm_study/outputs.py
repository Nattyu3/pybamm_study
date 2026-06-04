import csv
from pathlib import Path


def save_raw_solution_csv(
    path: Path,
    time_s,
    voltage_v,
    current_a,
    capacity_ah,
):
    """
    PyBaMM solution から取り出した基本時系列データをCSV保存する。
    """
    with path.open("w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(
            [
                "time_s",
                "voltage_V",
                "current_A",
                "discharge_capacity_Ah_raw",
            ]
        )

        for t, v, i, cap in zip(time_s, voltage_v, current_a, capacity_ah):
            writer.writerow([t, v, i, cap])


def save_capacity_voltage_csv(
    path: Path,
    discharge_specific_capacity,
    discharge_voltage_v,
    charge_specific_capacity,
    charge_voltage_v,
):
    """
    容量-電圧プロット用のCSVを保存する。
    """
    with path.open("w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["branch", "specific_capacity_mAh_g", "voltage_V"])

        for q, v in zip(discharge_specific_capacity, discharge_voltage_v):
            writer.writerow(["discharge", q, v])

        for q, v in zip(charge_specific_capacity, charge_voltage_v):
            writer.writerow(["charge", q, v])


def save_info(path: Path, lines: list[str]):
    """
    実験条件や使用変数などのメタ情報をテキスト保存する。
    """
    path.write_text("\n".join(lines) + "\n")
