from usecases.search_movie import MovieSearcher
from config.config import Config

config = Config()

if __name__ == "__main__":
    movie_searcher = MovieSearcher(config=config)
    movie_searcher.search(
        query="Plot same as Nolan directed"
    )