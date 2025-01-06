import logging
from fastapi import APIRouter, HTTPException, Query
from app.services.query_service import query_pinecone
from app.models.health_check_model import HealthCheckInput
from app.services.health_check_service import compare_metrics
from app.models.pitch_deck_model import PitchDeckInput
from app.services.pitch_deck_service import generate_pitch_deck
from app.services.history_service import add_history_entry, get_user_history
from typing import List, Dict
from app.models.history_model import HistoryEntry


router = APIRouter()

@router.get("/health", tags=["Health Check"])
async def health_check():
    """
    Check if the backend is running.
    """
    return {"status": "OK", "message": "Backend is running successfully."}

@router.get("/query", tags=["Query"])
async def query_endpoint(query: str = Query(..., description="The user's query")):
    """
    Process user queries, search in Pinecone, and generate answers using OpenAI.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required.")
    
    answer = query_pinecone(query)
    return {"query": query, "response": answer}

@router.post("/health-check/analyze", response_model=dict)
def health_check_analysis(input_data: HealthCheckInput):
    """
    Analyze startup metrics against benchmark data and summarize with LLM.
    """
    try:
        result = compare_metrics(input_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/pitch_deck", tags=["Pitch Deck"])
async def create_pitch_deck(input: PitchDeckInput):
    """
    Endpoint to generate a startup pitch deck.
    """
    result = generate_pitch_deck(
        name=input.name,
        domain=input.domain,
        problem=input.problem,
        solution=input.solution,
        founders=input.founders
    )

    if not result:
        raise HTTPException(status_code=500, detail="Failed to generate pitch deck.")
    
    return {"pitch_deck": result}


@router.post("/history", tags=["History"])
async def add_entry(entry: HistoryEntry):
    """
    Add a history entry for the authenticated user.
    """
    try:
        add_history_entry(
            user_id=entry.user_id,
            entry_type=entry.type,
            input_data=entry.input,
            output=entry.output
        )
        return {"message": "History entry added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{user_id}")
async def user_history(user_id: str):
    """
    Fetch user history.
    """
    try:
        history = get_user_history(user_id)
        if not history:
            logging.info(f"No history found for user: {user_id}")
            return {"user_id": user_id, "history": []} 
        return {"user_id": user_id, "history": history}
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Unexpected error fetching history for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")