import numpy as np
import json
import regex as re
from typing import Any, Optional, Dict


def return_none_when_is_nan(value: Any) -> Optional[Any]:
    try:
        np.isnan(value)
    except TypeError:
        return value
    
    if np.isnan(value):
        return None
    return value


def convert_text_to_json(text: str) -> Dict[str, Any]:
    json_data = {}
    pattern = r"\{.*\}"

    match = re.search(pattern, text, re.DOTALL)

    if match:
        json_str = match.group()
        json_str = json_str.replace("None", "null").replace("False", "false").replace("True", "true")
        json_str = json_str.strip("` \n").replace("json", "").strip()
        json_data = json.loads(json_str)
    return json_data