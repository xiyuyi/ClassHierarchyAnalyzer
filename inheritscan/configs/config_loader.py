import json
import os
from pathlib import Path

import inheritscan

package_path = Path(inheritscan.__file__).parent


def load_json_config(name="logger_config") -> dict:
    if name == "logger_config":
        path = package_path / "configs" / "log_configs.json"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing config file: {path}")
        with open(path, "r") as f:
            return json.load(f)
