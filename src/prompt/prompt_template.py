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
    same_attributes_as (bool): The query requires to find others similar movie or not. If requires answer true

    Note: from each above metadata, If can't extract, please answer null

    return the metadata in json format
    query: {query}
    """
    return prompt