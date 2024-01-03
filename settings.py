import argparse
from argparse import Namespace
from typing import Dict

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma

from type_extensions import T


def parse_args() -> Namespace:
    # Commandline arguments
    parser = argparse.ArgumentParser(description="Arguments for R2CBR3H-SR RAG")
    ################################ RBHSR RAG parameters ###########################
    parser.add_argument("--feature", default="fbank", type=str)
    parser.add_argument("--top_n_rerank", default=3, type=int)
    parser.add_argument("--iteration", default=0, type=int)
    parser.add_argument("--max_iterations", default=2, type=int)
    parser.add_argument("--chunk_size", default=500, type=int)
    parser.add_argument("--chunk_overlap", default=0, type=int)
    parser.add_argument("--vector_store", default=Chroma)
    parser.add_argument("--name", default="./doc/", type=str)
    # parser.add_argument("--persist_dir", default="/data/", type=str)
    parser.add_argument("--persist_dir", default="db", type=str)

    args = parser.parse_args()
    return args


def parse_kwargs() -> Dict[str, T]:
    vdb = {"glob": "./*.txt", "loader_cls": TextLoader}
    llm = {"model": "gpt-3.5-turbo-1106", "temperature": 0, "max_tokens": 2000}
    bs = {"response_format": {"type": "json_object"}} | llm
    st = {"response_format": {"type": "json_object"}} | llm

    vector_store = Chroma
    source_loader = DirectoryLoader
    splitter = RecursiveCharacterTextSplitter

    return {
        "vdb": vdb,
        "llm": llm,
        "bs": bs,
        "st": st,
        "vector_store": vector_store,
        "source_loader": source_loader,
        "splitter": splitter,
    }
