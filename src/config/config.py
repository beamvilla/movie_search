from typing import Mapping, Union, List

from utils import load_yaml_file


class OpensearchConfig:
    def __init__(self, _config: Mapping[str, Union[str, int, List[str]]]) -> None:
        self.host = _config["HOST"]
        self.port = _config["PORT"]
        self.user_env = _config["USER_ENV"]
        self.user_password_env = _config["USER_PASSWORD_ENV"]
        self.model_id = _config["MODEL_ID"]
        self.excludes = _config["EXCLUDES"]
        self.k = _config["K"]
        self.size = _config["SIZE"]
        self.index_name = _config["INDEX_NAME"]
        self.hybrid_search_pipeline_name = _config["HYBRID_SEARCH_PIPELINE_NAME"]


class Config:
    def __init__(self, config_path: str = "./config/config.yaml") -> None:
        self.config_file = load_yaml_file(config_path)
        self.opensearch_config = OpensearchConfig(self.config_file["OPENSEARCH_CONFIG"])
