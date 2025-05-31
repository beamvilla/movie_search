import pandas as pd
from dotenv import load_dotenv
from typing import Optional
from tqdm import tqdm

from src.utils.common import return_none_when_is_nan
from repository.opensearch import OpensearchRepository, LOCALHOST, OPENSEARCH_PORT


class OpensearchIndexer:
    def __init__(
        self,
        index_name: str,
        dataset_path: str,
        opensearch_host: str = LOCALHOST,
        opensearch_port: int = OPENSEARCH_PORT,
        opensearch_user_env: str = "user",
        opensearch_password_env: str = "password"
    ) -> None:
        load_dotenv()

        self.movie_df = pd.read_csv(dataset_path)
        self.opensearch_repo = OpensearchRepository(
            host=opensearch_host,
            port=opensearch_port,
            user_env=opensearch_user_env,
            password_env=opensearch_password_env
        )
        self.index_name = index_name

    def send_data_to_index(self, limit: Optional[int] = None):
        if limit is None:
            limit = len(self.movie_df)

        idx = 1

        for row in tqdm(limit):
            genres_text = None
            plot_keywords_text = None
            movie_description = None

            movie_title     = return_none_when_is_nan(self.movie_df.loc[row, "movie_title"])
            director_name   = return_none_when_is_nan(self.movie_df.loc[row, "director_name"])
            movie_imdb_link = return_none_when_is_nan(self.movie_df.loc[row, "movie_imdb_link"])
            content_rating  = return_none_when_is_nan(self.movie_df.loc[row, "content_rating"])
            genres          = return_none_when_is_nan(self.movie_df.loc[row, "genres"])

            if genres is not None:
                genres = genres.split("|")
                genres_text = ", ".join(genres)

            plot_keywords= return_none_when_is_nan(self.movie_df.loc[row, "plot_keywords"])
            if plot_keywords is not None:
                plot_keywords = plot_keywords.split("|")
                plot_keywords_text = ", ".join(plot_keywords)
                
            title_year = return_none_when_is_nan(self.movie_df.loc[row, "title_year"])

            if title_year is not None:
                title_year = str(int(title_year))

            if movie_title is not None:
                movie_description = f"{movie_title} is a {title_year} {genres_text} movie directed by {director_name}. Keywords: {plot_keywords_text}. Rated {content_rating}."
            
            json_data = {
                "id": str(idx),
                "movie_title": movie_title.strip(),
                "director_name": director_name.strip(),
                "genres": genres,
                "plot_keywords": plot_keywords,
                "title_year": title_year,
                "movie_imdb_link": movie_imdb_link,
                "content_rating": content_rating,
                "movie_description": movie_description
            }
            response = self.opensearch_repo.send_request(
                method="put",
                endpoint=f"{self.index_name}/_doc/{idx}",
                json_data=json_data
            )
            idx += 1
    

if __name__ == "__main__":
    opensearch_indexer = OpensearchIndexer(
        index_name="movie-search-index",
        dataset_path="./data/movie_dataset.csv",
        opensearch_host="https://localhost",
        opensearch_port=9200,
        opensearch_user_env="opensearch_user",
        opensearch_password_env="opensearch_password"
    )
    opensearch_indexer.send_data_to_index(limit=200)