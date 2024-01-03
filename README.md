# Concurrent Brainstorming \& Hypothesis Satisfying: An Iterative Framework for Enhanced Retrieval-Augmented Generation (R2CBR3H-SR)

The implementation of: ``**Concurrent Brainstorming \& Hypothesis Satisfying: An Iterative Framework for Enhanced Retrieval-Augmented Generation (R2CBR3H-SR)''**. The link to the arxiv paper will be provided soon.

## Description

This study presents a novel method for enhancing question-answering systems with retrieval-augmented generation capabilities. Our approach incorporates a cyclical process that melds cutting-edge developments in natural language processing with sophisticated information retrieval techniques. The core elements of our architecture include:

1. **Concurrent Brainstorming**: In this initial phase, we utilize the input question to simultaneously provoke the creation of semantically akin queries using a concurrent search across a document vector database.

2. **Iterative Reranking**: After the brainstorming period, the leading vector database results are selectively reranked, setting the stage for the upcoming formulation phase.

3. **Hybrid Hypothesize-Satisfying**: Employing a chain-of-thought prompting strategy, this phase combines forming hypotheses with the notion of satisfying, aiming to fulfill the user's quest for knowledge efficiently.

4. **Refinement**: The concluding phase distills the brainstormed ideas and queries into a refined, compact form that focuses on information-rich content over excess elaboration.

## Installation

Install all the necessary requirements.

```sh
pip install -r requirements.txt
```

## Environment Variables

Create a .env file and set your ```openai``` and ```cohere``` API keys.

## Data

### Download

You can get the .txt documents by running the following command.

```sh
wget -q https://www.dropbox.com/s/vs6ocyvpzzncvwh/new_articles.zip
```

Then, unzip the downloaded documents and put them in the ```doc``` directory.

```sh
unzip -q new_articles.zip -d doc
```

We have already provided the ```doc``` directory, so you do not need to download it again.

### Ingestion

Set the appropriate parameters according to your need in ```settings.py```. Make sure that the ```persist_dir``` in ```settings.py``` is set to "db" if you are not going to use docker later on, otherwise set it to "/data/". 

To ingest the documents, run the following command.

```sh
python data_ingestion.py
```

### Dataset for Evaluation

We have already provided the sets of questions and answers for you in the ```qa_db``` to be used for evaluating the performance of the proposed method and comparing with the baseline.

## Interact with Documents using the Proposed Method

To interact with the ingested documents using the proposed method, run the following command.

```sh
python main_proposed.py
```

To interact with the ingested documents using the baseline method, run the following command.

```sh
python main_baseline.py
```

To use the docker compose for interacting with your documents, use the following command to build, (re)create, start, and attach to containers for a service in detached mode.

```sh
docker compose up -d
```

To follow log output(s) from containers use the following command.

```sh
docker compose logs -f
```

To stop and remove container(s), network(s), volume(s), and image(s) created by `up`, use the following command.

```sh
docker compose down -v
```

## Post Processing

To analyze the performance and compare the results with the baseline according to the results obtained by the simulations and saved in the directories ```results``` and ```results_baseline```, run the following.

```sh
python results_post_processing.py
```

## Author

Arash Shahmansoori (arash.mansoori65@gmail.com)

## License

This project is licensed under the terms of the [MIT License](LICENSE)