import csv
from pathlib import Path
from typing import Any

from pybamm_study.plotting import plot_capacity_voltage


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


def save_capacity_voltage_result(
    out_dir: Path,
    prefix: str,
    data: dict[str, Any],
    branches: dict[str, Any],
    discharge_specific_capacity,
    charge_specific_capacity,
    info_lines: list[str],
    plot_title: str,
    ylim: tuple[float, float] | None = None,
) -> dict[str, Path]:
    """
    容量-電圧シミュレーション結果一式を保存する。

    保存するもの:
    - raw solution CSV
    - capacity-voltage CSV
    - capacity-voltage PNG
    - info TXT

    Parameters
    ----------
    out_dir:
        保存先ディレクトリ。
    prefix:
        出力ファイル名の接頭辞。
        例: prefix="li" の場合、
        li_raw_solution.csv, li_capacity_voltage.csv などを作る。
    data:
        extract_basic_solution() で取り出した基本データ。
        必須キー:
        - time_s
        - voltage_v
        - current_a
        - capacity_ah
    branches:
        split_discharge_charge() で分離した充放電データ。
        必須キー:
        - discharge_voltage_v
        - charge_voltage_v
    discharge_specific_capacity:
        放電側の比容量 [mAh/g]。
    charge_specific_capacity:
        充電側の比容量 [mAh/g]。
    info_lines:
        info.txt に書き込むメタ情報。
    plot_title:
        グラフタイトル。
    ylim:
        y軸範囲。例: (2.0, 4.4)

    Returns
    -------
    dict[str, Path]
        保存したファイルパス一覧。
    """
    raw_csv_path = out_dir / f"{prefix}_raw_solution.csv"
    plot_csv_path = out_dir / f"{prefix}_capacity_voltage.csv"
    png_path = out_dir / f"{prefix}_capacity_voltage.png"
    info_path = out_dir / f"{prefix}_info.txt"

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
        title=plot_title,
        ylim=ylim,
    )

    save_info(
        info_path,
        info_lines
        + [
            f"plot csv = {plot_csv_path.name}",
            f"raw csv = {raw_csv_path.name}",
            f"png = {png_path.name}",
        ],
    )

    return {
        "plot_csv": plot_csv_path,
        "raw_csv": raw_csv_path,
        "png": png_path,
        "info": info_path,
    }
