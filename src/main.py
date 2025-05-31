from usecases.search_movie import MovieSearcher


if __name__ == "__main__":
    movie_searcher = MovieSearcher()
    movie_searcher.extract_query_metadata(query="Directed by Christopher Nolan with dream plot")