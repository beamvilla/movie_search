from typing import Dict, Union, Optional, Tuple
import json
import regex as re
import requests

from repository.openai import OpenAIRepository
from .search_query_format import *
from prompt.prompt_template import *
from utils.common import convert_text_to_json
from utils.log_utils import get_logger
from repository.opensearch import OpensearchRepository
from config.config import Config, GPTModelConfig


class MovieSearcher:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.openai_repo = OpenAIRepository()
        self.opensearch_config = self.config.opensearch_config
        self.openai_config = self.config.openai_config

        self.opensearch_repo = OpensearchRepository(
            config=self.opensearch_config
        )
        
        self.movie_index_name = self.opensearch_config.index_name

    def extract_query_metadata(
        self, 
        query: str,
        model_config: GPTModelConfig
    ) -> Dict[str, str]:
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
            model_config=model_config
        )
        try:
            query_metadata = convert_text_to_json(response)
        except Exception as err:
            get_logger().error(err)
            get_logger().info("Response: ", response)
            return query_metadata
        
        return query_metadata
    
    def get_search_results(self, search_response: requests.Response) -> List[Mapping[str, Any]]:
        status_code = search_response.status_code
        if status_code == 200:
            search_results = json.loads(search_response.content.decode("utf-8"))
            search_results = search_results["hits"]["hits"]
            return search_results

        get_logger().error("Search error with status_code: ", status_code)
        return []
    
    def search_with_same_attribute(
        self,
        query: str,
        movie_title: Optional[str],
        director_name: Optional[str]
    ):
        filter_list = []
        if movie_title is not None:
            filter_list.append({
                "term": {
                    "movie_title": {
                        "value": movie_title,
                        "case_insensitive": True
                    }
                }
            })
        
        if director_name is not None:
            filter_list.append({
                "term": {
                    "director_name": {
                        "value": director_name,
                        "case_insensitive": True
                    }
                }
            })

        search_query = get_semantic_search_with_must_not_term_format(
            query_text=query,
            model_id=self.opensearch_config.model_id,
            filter_list=filter_list,
            excludes_fields=self.opensearch_config.excludes,
            k=self.opensearch_config.k,
            size=self.opensearch_config.size
        )
        search_response = self.opensearch_repo.send_request(
            method="get",
            endpoint=f"{self.movie_index_name}/_search",
            json_data=search_query
        )    
        search_results = self.get_search_results(search_response=search_response)
        return search_results
    
    def search_agent(
        self, 
        query_metadata: Dict[str, Union[str, List[str], bool]],
        query: str
    ) -> List[Dict[str, Any]]:
        movie_title = query_metadata["movie_title"]
        director_name = query_metadata["director_name"]
        same_attributes_as = query_metadata["same_attributes_as"]

        if same_attributes_as is True and \
            (movie_title is not None or director_name is not None):
            return self.search_with_same_attribute(
                query=query,
                movie_title=movie_title,
                director_name=director_name
            )
        
    def summarize_search(
        self, 
        query: str,
        search_results: List[Dict[str, Any]],
        model_config: GPTModelConfig
    ) -> str:
        all_search_movie_description_results = "- "
        n_results = len(search_results)

        for i, search_result in enumerate(search_results):
            movie_description = search_result["_source"]["movie_description"]
            all_search_movie_description_results += movie_description

            if i < n_results - 1:
                all_search_movie_description_results += "\n- "

        prompt = get_summarize_search_results_prompt(
            query=query,
            all_search_movie_description_results=all_search_movie_description_results
        )
        summarized_search_results = self.openai_repo.send_request(
            prompt=prompt,
            model_config=model_config
        )
        return summarized_search_results
    
    def rerank(
        self,
        query: str, 
        documents: List[Mapping[str, Any]]
    ) -> List[Mapping[str, Any]]:
        get_logger().info("Reranking search results with LLM.")
        results = []
        for doc in documents:
            description = doc["_source"]["movie_description"]
            prompt = get_rerank_prompt(query=query, description=description)
            reranked_score_result = self.openai_repo.send_request(
                prompt=prompt, 
                model_config=self.openai_config.reranker
            )
            match = re.search(r"Total score:\s*(\d+)", reranked_score_result)

            if match:
                reranked_score = int(match.group(1))
            else:
                get_logger().error("Rerank LLM answer wrong format with : ", reranked_score_result)
                reranked_score = 0
            results.append((reranked_score, doc))
        
        sorted_reranked_score_results = sorted(results, key=lambda x: x[0], reverse=True)
        sorted_documents = [doc for _, doc in sorted_reranked_score_results]
        return sorted_documents

    def search(self, query: str):
        summarized_search_results = None
        
        # query_metadata = self.extract_query_metadata(
        #     query=query,
        #     model_config=self.openai_config.extract_query_metadata_model
        # )
       
        query_metadata = {'movie_title': 'Avatar', 'director_name': None, 'genres': None, 'keywords': ['plot', 'like', 'Avatar'], 'year': None, 'content_rating': None, 'same_attributes_as': True}

        search_results = self.search_agent(
            query_metadata=query_metadata,
            query=query
        )

        if self.config.rerank_search is True:
            search_results = self.rerank(
                query=query,
                documents=search_results
            )
        
        if self.config.summarize_search is True:
            summarized_search_results = self.summarize_search(
                query=query,
                search_results=search_results,
                model_config=self.openai_config.summarize_search
            )
            print(summarized_search_results)


           