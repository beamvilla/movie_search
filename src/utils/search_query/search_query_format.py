from typing import List, Dict, Any, Mapping


def get_semantic_search_format(
    query_text: str,
    embedding_field: str,
    model_id: str,
    excludes_fields: List[str] = [],
    k: int = 100,
    size: int = 100
) -> Dict[str, Any]:
    return {
        "_source": {
            "excludes": excludes_fields
        },
        "query": {
            "neural": {
                embedding_field: {
                    "query_text": query_text,
                    "k": k,
                    "model_id": model_id
                }
            }
        },
        "size": size
    }


def get_filter_search_format(
    filter_list: List[Mapping[str, Any]],
    excludes_fields: List[str] = [],
    size: int = 100
) -> Dict[str, Any]:
    return {
        "_source": {
            "excludes": excludes_fields
        },
        "query": {
            "bool": {
                "filter": filter_list
            }
        },
        "size": size
    }


def get_hybrid_search_format(
    query_text: str,
    text_field: str,
    embedding_field: str,
    model_id: str,
    excludes_fields: List[str] = [],
    k: int = 100,
    size: int = 100
):
    return {
        "_source": {
            "excludes": excludes_fields
        },
        "query": {
            "hybrid": {
                "queries": [
                    {
                        "match": {
                            text_field: {
                                "query": query_text
                            }
                        }
                    },
                    {
                        "neural": {
                            embedding_field: {
                                "query_text": query_text,
                                "model_id": model_id,
                                "k": k
                            }
                        }
                    }
                ]
            }
        },
        "size": size
    }
