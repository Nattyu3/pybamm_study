from datetime import datetime
from pathlib import Path


def project_root() -> Path:
    """
    プロジェクトルートを返す。

    想定:
        project/
        └── src/
            └── pybamm_study/
                └── paths.py
    """
    return Path(__file__).resolve().parents[2]


def make_output_dir(prefix: str | None = None) -> Path:
    """
    results/以下にタイムスタンプ付き出力ディレクトリを作成する。
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    if prefix:
        dirname = f"{timestamp}_{prefix}"
    else:
        dirname = timestamp

    out_dir = project_root() / "results" / dirname
    out_dir.mkdir(parents=True, exist_ok=False)

    return out_dir
