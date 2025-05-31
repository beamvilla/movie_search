import requests
from requests.auth import HTTPBasicAuth 
from typing import Mapping, Any
from dataclasses import dataclass


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


def send_request(
    method: str,
    user: str,
    password: str,
    endpoint: str,
    json_data: Mapping[str, Any] = {},
    host: str = LOCALHOST,
    port: int = OPENSEARCH_PORT
) -> requests.Response:
    url = f"{host}:{port}/{endpoint}"
    auth = HTTPBasicAuth(user, password)
    response = REQUEST_METHOD[method](
        url=url,
        json=json_data,
        headers=JSON_HEADERS,
        auth=auth,
        verify=False
    )
    return response


def delete(
    user: str,
    password: str,
    endpoint: str,
    host: str = LOCALHOST,
    port: int = OPENSEARCH_PORT
) -> requests.Response:
    url = f"{host}:{port}/{endpoint}"
    auth = HTTPBasicAuth(user, password)
    response = requests.delete(
        url=url,
        auth=auth,
        verify=False
    )
    return response