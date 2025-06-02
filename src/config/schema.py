from typing import List, Optional
from pydantic import BaseModel, Field


class MovieSource(BaseModel):
    plot_keywords: Optional[List[str]]
    movie_imdb_link: Optional[str]
    genres: Optional[List[str]]
    director_name: Optional[str]
    content_rating: Optional[str]
    title_year: Optional[str]
    id: Optional[str]
    movie_title: Optional[str]
    movie_description: Optional[str]


class MovieResultItem(BaseModel):
    index: str = Field(..., alias="_index")
    id: str = Field(..., alias="_id")
    score: float = Field(..., alias="_score")
    source: MovieSource = Field(..., alias="_source")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True  # For compatibility with Pydantic v2+
        arbitrary_types_allowed = True


class APIResponseBody(BaseModel):
    success: bool
    search_results: List[MovieResultItem]
    search_summarize: Optional[str]


class SearchRequest(BaseModel):
    query: str