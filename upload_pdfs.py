import os
from app.services.embedding_service import upload_document_to_pinecone
from app.utils.document_loader import extract_text_from_pdf
from app.utils.logger import logger

# Directory paths
RAW_DOCS_DIR = "data/"
PROCESSED_DOCS_DIR = "data/processed"

def process_and_upload_pdfs():
    """
    Process all PDF files in the sample_docs folder and upload them to Pinecone.
    """
    if not os.path.exists(PROCESSED_DOCS_DIR):
        os.makedirs(PROCESSED_DOCS_DIR)
    
    pdf_files = [f for f in os.listdir(RAW_DOCS_DIR) if f.endswith(".pdf")]
    
    if not pdf_files:
        logger.info("No PDF files found to process.")
        return
    
    for pdf_file in pdf_files:
        file_path = os.path.join(RAW_DOCS_DIR, pdf_file)
        try:
            logger.info(f"Processing PDF: {pdf_file}")
            upload_document_to_pinecone(file_path, {"name": pdf_file})
            
            # Move the processed file to the processed folder
            processed_path = os.path.join(PROCESSED_DOCS_DIR, pdf_file)
            os.rename(file_path, processed_path)
            logger.info(f"Successfully uploaded and moved {pdf_file}")
        
        except Exception as e:
            logger.error(f"Failed to process {pdf_file}: {str(e)}")

if __name__ == "__main__":
    process_and_upload_pdfs()
