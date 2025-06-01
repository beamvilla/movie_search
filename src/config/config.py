from typing import Mapping, Union, List

from utils import load_yaml_file


class GPTModelConfig:
    def __init__(self, _config: Mapping[str, Union[str, float]]) -> None:
        self.model = _config["MODEL"]
        self.temperature = _config["TEMPERATURE"]


class OpenAIConfig:
    def __init__(self, _config: Mapping[str, str]) -> None:
        self.extract_query_metadata_model = GPTModelConfig(_config=_config["EXTRACT_QUERY_METADATA_MODEL"])
        self.summarize_search = GPTModelConfig(_config=_config["SUMMARIZE_SEARCH"])
        self.reranker = GPTModelConfig(_config=_config["RERANKER"])


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
        config_file = load_yaml_file(config_path)
        self.opensearch_config = OpensearchConfig(config_file["OPENSEARCH_CONFIG"])
        self.openai_config = OpenAIConfig(config_file["OPENAI_CONFIG"])
        
        self.summarize_search = config_file["SUMMARIZE_SEARCH"]
        self.extract_query_metadata = config_file["EXTRACT_QUERY_METADATA"]
        self.rerank_search = config_file["RERANK_SEARCH"]
