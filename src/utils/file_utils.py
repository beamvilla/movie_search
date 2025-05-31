import yaml
from typing import Dict, Any


def load_yaml_file(yaml_file_path: str) -> Dict[str, Any]:
    with open(yaml_file_path) as f:
        try:
            yaml_file = yaml.safe_load(f)
        except yaml.YAMLError:
            raise
    return yaml_file