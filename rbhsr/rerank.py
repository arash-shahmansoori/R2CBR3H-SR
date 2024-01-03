import os

import cohere
import dotenv

dotenv.load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))
