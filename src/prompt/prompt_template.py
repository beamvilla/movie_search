def get_extract_query_metadata_prompt(query: str) -> str:
    prompt = f"""
    From a given query, please extract metadata.

    Each metadata details are:
    movie_title (str): movie name
    director_name (str): director name
    genres (List[str]): all genres which found in query
    keywords (List[str]): keywords which related a movie
    year (str): year found
    content_rating (str): Motion picture content rating system auch as 'PG-13', 'PG', 'G', 
        'R', nan, 'TV-14', 'TV-PG', 'TV-MA', 'TV-G',
       'Not Rated', 'Unrated', 'Approved', 'TV-Y', 'NC-17', 'X', 'TV-Y7',
       'GP', 'Passed', 'M'
    same_attributes_as (bool): Return true only if the user query explicitly asks to find movies similar 
    to a specific movie title, director name or movie mentioned in the query, such as queries containing phrases like 
    "movie like <movie_title>", "similar to <movie_title>", or "movies similar to <movie_title>". 

    Note: from each above metadata, If can't extract, please answer null

    return the metadata in json format
    query: {query}
    """
    return prompt


def get_summarize_search_results_prompt(
    query: str,
    all_search_movie_description_results: str
) -> str:
    return f"""
    You are a helpful assistant. 
    The user searched for movies with the query: '{query}'. 
    Based on the following movie descriptions from the search results, 
    generate a short, user-friendly summary (2–3 sentences) that explains what kind of movies are shown:
    
    all search movie description results:
    {all_search_movie_description_results}
    """


def get_rerank_prompt(query: str, description: str) -> str:
    return f"""
    Rate the relevance of this description for the given query.
    Consider these aspects:
    - Direct answer relevance (0-5)
    - Information completeness (0-3)
    - Factual accuracy (0-2)
    
    Query: {query}
    Description: {description}
    
    Provide scores for each aspect and a total score out of 10.
    """