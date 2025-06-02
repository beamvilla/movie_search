from fastapi import FastAPI

from src.usecases.search_movie import MovieSearcher
from src.config.schema import APIResponseBody, SearchRequest
from src.config.config import Config


config = Config()
app = FastAPI()

@app.post(
    "/search_movie", 
    response_model=APIResponseBody
)
async def search_movie(query: SearchRequest):
    movie_searcher = MovieSearcher(config=config)
    search_results, search_summarize = movie_searcher.search(
        query=query
    )
    return {
        "success": True,
        "search_results": search_results,
        "search_summarize": search_summarize
    }