import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv()


def create_client():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return client
