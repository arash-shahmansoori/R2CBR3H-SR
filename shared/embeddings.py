import os

import dotenv
from langchain.embeddings.openai import OpenAIEmbeddings

dotenv.load_dotenv()


def create_openai_embedding() -> OpenAIEmbeddings:
    openai_embedding = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    return openai_embedding
