import sys
sys.path.append("./")

from usecases.send_data_to_opensearch_index import OpensearchIndexer


if __name__ == "__main__":
    opensearch_indexer = OpensearchIndexer(
        dataset_path="./data/movie_dataset.csv"
    )
    opensearch_indexer.send_data_to_index(limit=200)