import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth 
from typing import Mapping, Any
from dataclasses import dataclass

from config.config import OpensearchConfig


JSON_HEADERS = {"Content-Type": "application/json; charset=UTF-8"}
REQUEST_METHOD = {
    "put": requests.put,
    "post": requests.post,
    "get": requests.get
}
LOCALHOST = "http://localhost"
OPENSEARCH_PORT = 9200


@dataclass
class APIConfig:
    host: str
    port: int
    user: str
    password: str


class OpensearchRepository:
    def __init__(
        self,
        config: OpensearchConfig
    ) -> None:
        load_dotenv()

        self.user = os.getenv(config.user_env)
        self.__password = os.getenv(config.user_password_env)
        self.host = config.host
        self.port = config.port
    
    def send_request(
        self,
        method: str,
        endpoint: str,
        json_data: Mapping[str, Any] = {}
    ) -> requests.Response:
        url = f"{self.host}:{self.port}/{endpoint}"
        auth = HTTPBasicAuth(self.user, self.__password)
        response = REQUEST_METHOD[method](
            url=url,
            json=json_data,
            headers=JSON_HEADERS,
            auth=auth,
            verify=False
        )
        return response


    def delete(
        self,
        endpoint: str
    ) -> requests.Response:
        url = f"{self.host}:{self.port}/{endpoint}"
        auth = HTTPBasicAuth(self.user, self.__password)
        response = requests.delete(
            url=url,
            auth=auth,
            verify=False
        )
        return response