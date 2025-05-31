from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, Union, List, Dict

from utils.log_utils import get_logger


class OpenAIRepository:
    def __init__(self) -> None:
        load_dotenv()

        self.client = OpenAI()
    
    def send_request(
        self, 
        prompt: Union[List[Dict[str, str]], str],
        model: str = "gpt-4.1"
    ) -> Optional[str]:
        try:
            response = self.client.responses.create(
                model=model,
                input=prompt
            )
        except Exception as err:
            get_logger().error("Error to send request to OpenAI")
            return None
        return response.output_text
