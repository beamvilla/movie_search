from typing import Dict, Union, Optional, Tuple
import json
import regex as re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        self.hybrid_search_pipeline = self.opensearch_config.hybrid_search_pipeline_name

    def all_metadata_is_none(self, metadata: Mapping[str, Union[str, bool, List[str]]]) -> bool:
        for value in metadata.values():
            if value is True:
                return False
            
            if value is not None:
                return False
        return True
    
    def extract_query_metadata(
        self, 
        query: str,
        model_config: GPTModelConfig
    ) -> Optional[Dict[str, str]]:
        get_logger().info("Extracting metadata from query.")
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
            return None
        
        if self.all_metadata_is_none(query_metadata) is None:
            return None
        
        return query_metadata
    
    def get_search_results(
        self, 
        search_query: Dict[str, Any],
        endpoint: str
    ) -> List[Mapping[str, Any]]:
        search_response = self.opensearch_repo.send_request(
            method="get",
            endpoint=endpoint,
            json_data=search_query
        )  
        status_code = search_response.status_code
        if status_code == 200:
            search_results = json.loads(search_response.content.decode("utf-8"))
            search_results = search_results["hits"]["hits"]
            return search_results

        get_logger().error("Search error with status_code: ", status_code)
        return []
    
    def search_with_same_attribute(
        self,
        movie_title: Optional[str],
        director_name: Optional[str],
        n_pick_attr: int = 5
    ) -> List[Mapping[str, Any]]:
        filter_list = []
        if movie_title is not None:
            filter_list.append(
                {
                    "term": {
                        "movie_title": {
                          "value": movie_title,
                          "case_insensitive": True
                        }
                    }
                }
            )
        
        if director_name is not None:
            filter_list.append(
                {
                    "term": {
                        "director_name": {
                          "value": director_name,
                          "case_insensitive": True
                        }
                    }
                }
            )

        # First filter x movies of the target attribute
        search_query = get_filter_search_format(
            filter_list=filter_list,
            excludes_fields=self.opensearch_config.excludes,
            size=n_pick_attr
        )

        size_per_each_result = self.opensearch_config.size // n_pick_attr
        target_attribute_ssearch_results = self.get_search_results(
            search_query=search_query,
            endpoint=f"{self.movie_index_name}/_search"
        )
        all_same_attribute_search_results = []
        
        # Use 5 movies description for find semantic search
        for target_attribute_ssearch_result in target_attribute_ssearch_results:
            movie_description = target_attribute_ssearch_result["_source"]["movie_description"]
            search_query = get_hybrid_search_with_must_not_term_format(
                query_text=movie_description,
                model_id=self.opensearch_config.model_id,
                filter_list=filter_list,
                excludes_fields=self.opensearch_config.excludes,
                k=self.opensearch_config.k,
                size=size_per_each_result
            )
            _search_results = self.get_search_results(
                search_query=search_query,
                endpoint=f"{self.movie_index_name}/_search?search_pipeline={self.hybrid_search_pipeline}"
            )
            all_same_attribute_search_results.extend(_search_results)
        return all_same_attribute_search_results
    
    def hybrid_search(
        self,
        query: str,
        filter_list: List[Mapping[str, Any]] = []
    ) -> List[Mapping[str, Any]]:
        search_query = get_hybrid_search_format(
            query_text=query,
            model_id=self.opensearch_config.model_id,
            excludes_fields=self.opensearch_config.excludes,
            k=self.opensearch_config.k,
            size=self.opensearch_config.size,
            filter_list=filter_list
        )
        search_results = self.get_search_results(
            search_query=search_query,
            endpoint=f"{self.movie_index_name}/_search?search_pipeline={self.hybrid_search_pipeline}"
        )
        return search_results
    
    def search_agent(
        self,
        query: str,
        query_metadata: Optional[Dict[str, Union[str, List[str], bool]]] = None
    ) -> List[Dict[str, Any]]:
        if query_metadata is None:
            return self.hybrid_search(query=query, filter_list=[])
        
        movie_title = query_metadata["movie_title"]
        director_name = query_metadata["director_name"]
        same_attributes_as = query_metadata["same_attributes_as"]
        genres = query_metadata["genres"]
        title_year = query_metadata["year"]
        content_rating = query_metadata["content_rating"]
        search_results = []

        filter_list = []

        if movie_title is not None:
            filter_list.append({"match": {"movie_title": movie_title}})
            
        if director_name is not None:
            filter_list.append({"match": {"director_name": director_name}})

        if genres is not None:
            for genre in genres:
                filter_list.append({"match": { "genres": genre}})

        if title_year is not None:
            filter_list.append({"term": {"title_year": title_year}})

        if content_rating is not None:
            filter_list.append({"term": {"content_rating": content_rating}})

        if same_attributes_as is True and \
            (movie_title is not None or director_name is not None):
                search_results = self.search_with_same_attribute(
                    movie_title=movie_title,
                    director_name=director_name
                )
                
        if len(search_results) == 0:
            search_results = self.hybrid_search(query=query, filter_list=filter_list)
        return search_results
        
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

    def search(self, query: str) -> Tuple[List[Mapping[str, Any]], Optional[str]]:
        summarized_search_results = None
        query_metadata = None

        if self.config.extract_query_metadata is True:
            query_metadata = self.extract_query_metadata(
                query=query,
                model_config=self.openai_config.extract_query_metadata_model
            )
            get_logger().info("Metadata found")
            get_logger().info(json.dumps(query_metadata, indent=4, ensure_ascii=False))
       
        query_metadata = {
            "movie_title": "harry potter",
            "director_name": None,
            "genres": None,
            "year": None,
            "content_rating": None,
            "same_attributes_as": True
        }

        search_results = self.search_agent(query_metadata=query_metadata, query=query)
       
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
        return search_results, summarized_search_results
            
           