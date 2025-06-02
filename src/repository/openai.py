from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, Union, List, Dict

from src.utils.log_utils import get_logger
from src.config.config import GPTModelConfig


class OpenAIRepository:
    def __init__(self) -> None:
        load_dotenv()

        self.client = OpenAI()
    
    def send_request(
        self, 
        prompt: Union[List[Dict[str, str]], str],
        model_config: GPTModelConfig
    ) -> Optional[str]:
        try:
            response = self.client.responses.create(
                model=model_config.model,
                input=prompt,
                temperature=model_config.temperature
            )
        except Exception as err:
            get_logger().error("Error to send request to OpenAI")
            return None
        return response.output_text
