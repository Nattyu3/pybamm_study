def estimate_active_material_mass_g(
    parameter_values,
    target_specific_capacity_mAh_g: float,
):
    """
    セルの公称容量から、比容量スケール用の仮想活物質質量を決める。
    """
    nominal_capacity_ah = parameter_values["Nominal cell capacity [A.h]"]
    nominal_capacity_mah = nominal_capacity_ah * 1000.0
    active_material_mass_g = nominal_capacity_mah / target_specific_capacity_mAh_g

    return active_material_mass_g, nominal_capacity_ah


def split_discharge_charge(voltage_v, current_a, capacity_ah):
    """
    電流の符号で放電/充電を分ける。

    PyBaMM/Chen2020では、多くの場合
    current > 0 が放電
    current < 0 が充電。
    """
    discharge_mask = current_a > 0
    charge_mask = current_a < 0

    discharge_capacity_ah = capacity_ah[discharge_mask]
    discharge_voltage_v = voltage_v[discharge_mask]

    charge_capacity_raw_ah = capacity_ah[charge_mask]
    charge_voltage_v = voltage_v[charge_mask]

    if len(discharge_capacity_ah) > 0:
        discharge_capacity_ah = discharge_capacity_ah - discharge_capacity_ah[0]

    if len(charge_capacity_raw_ah) > 0:
        charge_capacity_ah = abs(charge_capacity_raw_ah - charge_capacity_raw_ah[0])
    else:
        charge_capacity_ah = charge_capacity_raw_ah

    return {
        "discharge_capacity_ah": discharge_capacity_ah,
        "discharge_voltage_v": discharge_voltage_v,
        "charge_capacity_ah": charge_capacity_ah,
        "charge_voltage_v": charge_voltage_v,
    }


def to_specific_capacity_mAh_g(capacity_ah, active_material_mass_g: float):
    """
    容量 [A.h] を比容量 [mAh/g] に変換する。
    """
    return capacity_ah * 1000.0 / active_material_mass_g
