import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "knowhow-cloud-backend")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))

    # Pinecone Config
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV: str = os.getenv("PINECONE_ENV", "AWS_US_EAST_1")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME")

    # OpenAI Config
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    # Database Config
    MONGODB_URL = os.getenv("MONGODB_URL")


settings = Settings()
