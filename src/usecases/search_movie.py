from typing import Dict

from repository.openai import OpenAIRepository
from prompt.prompt_template import *
from utils.common import convert_text_to_json
from utils.log_utils import get_logger


class MovieSearcher:
    def __init__(self) -> None:
        self.openai_repo = OpenAIRepository()

    
    def extract_query_metadata(self, query: str) -> Dict[str, str]:
        query_metadata = {
            "movie_title": None,
            "director_name": None,
            "genres": None,
            "keywords": None,
            "year": None,
            "content_rating": None,
            "same_attributes_as": False
        }
        prompt = get_extract_query_metadata_prompt(query=query)
        response = self.openai_repo.send_request(
            prompt=prompt,
            model="gpt-4.1"
        )
        try:
            json_response = convert_text_to_json(response)
        except Exception as err:
            get_logger().error(err)
            get_logger().info("Response: ", response)
            return query_metadata
        
        print(json_response)



    def search(self, query: str):
        pass