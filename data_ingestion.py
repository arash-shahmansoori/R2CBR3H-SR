from data_ingestion import vec_db_persist
from settings import parse_args, parse_kwargs
from shared import create_openai_embedding


def main():
    args = parse_args()
    kwargs = parse_kwargs()

    vector_store = kwargs["vector_store"]
    kwargs_vdb = kwargs["vdb"]
    source_loader = kwargs["source_loader"]
    splitter = kwargs["splitter"]

    embedding = create_openai_embedding()

    _ = vec_db_persist(
        args.name,
        args.persist_dir,
        source_loader,
        splitter,
        args.chunk_size,
        args.chunk_overlap,
        vector_store,
        embedding,
        **kwargs_vdb,
    )


if __name__ == "__main__":
    main()
