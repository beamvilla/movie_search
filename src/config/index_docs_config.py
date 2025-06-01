from typing import Mapping, Union, List

from utils import load_yaml_file


class OpensearchConfig:
    def __init__(self, _config: Mapping[str, Union[str, int, List[str]]]) -> None:
        self.host = _config["HOST"]
        self.port = _config["PORT"]
        self.user_env = _config["USER_ENV"]
        self.user_password_env = _config["USER_PASSWORD_ENV"]
        self.model_id = _config["MODEL_ID"]
        self.index_name = _config["INDEX_NAME"]


class IndexDocsConfig:
    def __init__(self, config_path: str = "./config/index_docs_config.yaml") -> None:
        config_file = load_yaml_file(config_path)
        self.opensearch_config = OpensearchConfig(config_file["OPENSEARCH_CONFIG"])