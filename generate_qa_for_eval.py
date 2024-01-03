import json

from data_ingestion import generate_qa_dataset
from settings import parse_args, parse_kwargs


def main():
    kwargs = parse_kwargs()

    user_query = "Generate 10 questions and corresponding answers according to the provided documents below in JSON."

    subdoc_name = "subdoc_1_2"

    loader = kwargs["source_loader"](f"./docs_subdocs/{subdoc_name}/", **kwargs["vdb"])
    docs = loader.load()

    (response, elps_time), cb = generate_qa_dataset(user_query, docs, **kwargs["llm"])

    qa = json.loads(response)

    # Store the JSON data in a file
    with open(f"qa_db/{subdoc_name}/qa_dataset.json", "w") as file:
        json.dump(qa, file)

    print("Data stored successfully!")

    # print(elps_time, cb)


if __name__ == "__main__":
    main()
