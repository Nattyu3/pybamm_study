def get_entries(solution, candidates: list[str]):
    """
    PyBaMMの変数名ゆれに対応して、最初に見つかった変数を返す。
    """
    for name in candidates:
        try:
            return solution[name].entries, name
        except KeyError:
            pass

    raise KeyError(f"None of these variables were found: {candidates}")


def extract_basic_solution(solution):
    """
    よく使う基本変数をまとめて取り出す。
    """
    time_s, time_name = get_entries(solution, ["Time [s]"])

    voltage_v, voltage_name = get_entries(
        solution,
        ["Terminal voltage [V]", "Voltage [V]"],
    )

    current_a, current_name = get_entries(
        solution,
        ["Current [A]"],
    )

    capacity_ah, capacity_name = get_entries(
        solution,
        ["Discharge capacity [A.h]", "Throughput capacity [A.h]"],
    )

    data = {
        "time_s": time_s,
        "voltage_v": voltage_v,
        "current_a": current_a,
        "capacity_ah": capacity_ah,
    }

    names = {
        "time": time_name,
        "voltage": voltage_name,
        "current": current_name,
        "capacity": capacity_name,
    }

    return data, names
