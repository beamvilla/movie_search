from typing import List, Dict, Any, Mapping


def get_semantic_search_format(
    query_text: str,
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
                "movie_description_embedding": {
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
    model_id: str,
    excludes_fields: List[str] = [],
    k: int = 100,
    size: int = 100,
    filter_list: List[str] = []
) -> Dict[str, Any]:
    query_format = {
        "_source": {
            "excludes": excludes_fields
        },
        "query": {
            "hybrid": {
                "queries": [
                    {
                        "match": {
                            "movie_description": {
                                "query": query_text
                            }
                        }
                    },
                    {
                        "neural": {
                            "movie_description_embedding": {
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
    if len(filter_list) > 0:
       query_format["query"]["hybrid"]["filter"] = {
            "bool": {"must": filter_list}
        }
    return query_format


def get_semantic_search_with_must_not_term_format(
        
    query_text: str,
    model_id: str,
    filter_list: List[str] = [],
    excludes_fields: List[str] = [],
    k: int = 100,
    size: int = 100
) -> Dict[str, Any]:
    return {
        "_source": {
            "excludes": excludes_fields
        },
        "query": {
            "bool": {
                "must": {
                    "neural": {
                        "movie_description_embedding": {
                            "query_text": query_text,
                            "k": k,
                            "model_id": model_id
                        }
                    }
                },
                "must_not": filter_list
            }
        },
        "size": size
    }
 

def get_hybrid_search_with_must_not_term_format(
    query_text: str,
    model_id: str,
    filter_list: List[str] = [],
    excludes_fields: List[str] = [],
    k: int = 100,
    size: int = 100
) -> Dict[str, Any]:
    return {
        "_source": {
            "excludes": excludes_fields
        },
        "query": {
            "hybrid": {
                "queries": [
                    {
                        "match": {
                            "movie_description": {
                                "query": query_text
                            }
                        }
                    },
                    {
                        "neural": {
                            "movie_description_embedding": {
                                "query_text": query_text,
                                "model_id": model_id,
                                "k": k
                            }
                        }
                    }
                ],
                "filter": {
                    "bool": {
                        "must_not": filter_list
                    }
                }
            }
        },
        "size": size
    }