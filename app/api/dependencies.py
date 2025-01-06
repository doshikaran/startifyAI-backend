import os
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from app.config import settings

# Initialize Pinecone Instance
pc = Pinecone(
    api_key=settings.PINECONE_API_KEY
)

# Check and create the index if it doesn't exist
if settings.PINECONE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=settings.PINECONE_INDEX_NAME,
        dimension=1536, 
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-west-2'
        )
    )

# Connect to the index
index = pc.Index(settings.PINECONE_INDEX_NAME)

# Initialize OpenAI Client
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
