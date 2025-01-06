import json
from app.api.dependencies import index, openai_client
from app.utils.logger import logger

def query_pinecone(query: str, top_k: int = 5):
    """
    Process a user query, retrieve relevant chunks from Pinecone, and generate a response via OpenAI.
    """
    try:
        logger.info("Embedding the query...")
        # Embed the query using OpenAI
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=query
        )
        query_embedding = response.data[0].embedding
        
        logger.info("Performing similarity search in Pinecone...")
        # Perform similarity search in Pinecone
        search_results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        if not search_results.get('matches'):
            logger.warning("No relevant matches found in Pinecone.")
            return "No relevant information found."
        
        # Collect relevant chunks and combine them into a single context string
        context = "\n\n".join([
            f"[{match['metadata'].get('name', 'No Document Name')}]\n{match['metadata'].get('text', '')}" 
            for match in search_results['matches']
        ])
        
        logger.info("Generating answer with OpenAI...")
        # Pass the context to OpenAI for response generation
        completion_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing consice answers based on the given context."},
                {"role": "user", "content": f"Answer the query based on the following context:\n\n{context}\n\nQuery: {query}"}
            ],
            max_tokens=500,
            temperature=0.7,
            top_p=0.95
        )
        
        answer = completion_response.choices[0].message.content.strip()
        logger.info("Answer generated successfully.")
        return answer
    
    except Exception as e:
        logger.error(f"Failed to process query: {str(e)}")
        return "An error occurred while processing your query."

def summarize_with_llm(stage: str, analysis: dict) -> str:
    """Summarize health check analysis using LLM."""
    prompt = f"""
    You are an expert startup advisor. A startup at the {stage} stage provided financial metrics, and here are the benchmark comparisons:

    {json.dumps(analysis, indent=2)}

    Provide a clear, concise summary explaining the overall health of the startup, highlighting strengths and areas of improvement.
    """
    try:
        health_check_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant providing startup financial analysis summaries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7,
            top_p=0.95
        )
        # Accessing the response properly
        health_check_response_answer = health_check_response.choices[0].message.content.strip()
        logger.info("Summary generated successfully.")
        return health_check_response_answer
    except AttributeError as e:
        logger.error(f"AttributeError: {e}")
        return f"Failed to generate summary: AttributeError - {str(e)}"
    except Exception as e:
        logger.error(f"Exception: {e}")
        return f"Failed to generate summary: {str(e)}"