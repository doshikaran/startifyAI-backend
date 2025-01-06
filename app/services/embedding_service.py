from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.api.dependencies import index, openai_client
from app.utils.logger import logger
from app.utils.document_loader import extract_text_from_pdf

def upload_document_to_pinecone(file_path: str, metadata: dict):
    """
    Process a document, generate embeddings, and upload to Pinecone.
    """
    try:
        logger.info(f"Extracting text from {file_path}...")
        raw_text = extract_text_from_pdf(file_path)
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=9100, chunk_overlap=50)
        chunks = text_splitter.split_text("\n".join(raw_text))
        
        logger.info(f"Generated {len(chunks)} chunks from {file_path}.")
        
        # Embed and upload each chunk
        for i, chunk in enumerate(chunks):
            response = openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=chunk
            )
            embedding = response.data[0].embedding
            
            index.upsert(vectors=[{
                "id": f"{metadata['name']}_chunk_{i}",
                "values": embedding,
                "metadata": {
                    "name": metadata['name'],
                    "text": chunk  # Explicitly include chunk text
                }
            }])
        
        logger.info(f"Document '{metadata['name']}' successfully uploaded to Pinecone.")
    except Exception as e:
        logger.error(f"Failed to upload document '{metadata['name']}': {str(e)}")
        raise
