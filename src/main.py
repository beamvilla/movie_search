import json

from usecases.search_movie import MovieSearcher
from config.config import Config

config = Config()

if __name__ == "__main__":
    movie_searcher = MovieSearcher(config=config)
    search_results, summarized_search_results = movie_searcher.search(
        query="หนังที่คล้ายเรื่อง harry potter"
    )
    print("============== SEARCH RESULTS ==============\n")
    print(json.dumps(search_results, indent=4, ensure_ascii=False))
    print("\n\n============== SUMMARIZE ==============\n")
    print(summarized_search_results)