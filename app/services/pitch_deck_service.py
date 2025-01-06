import json
import re
from typing import Dict
from app.utils.logger import logger
from app.api.dependencies import openai_client


PITCH_DECK_DATA_PATH = "data/startup_health_check.json"

def load_pitch_deck_data() -> Dict:
    """Load health check data from JSON file."""
    with open(PITCH_DECK_DATA_PATH, "r") as file:
        return json.load(file)

def generate_pitch_deck(name: str, domain: str, problem: str, solution: str, founders: str) -> dict:
    """Generate a pitch deck using LLM."""
    try:
        prompt = f"""
        Create a startup pitch deck with the following details:
        - Startup Name: {name}
        - Domain: {domain}
        - Problem: {problem}
        - Solution: {solution}
        - Founders: {founders}

        Structure the pitch deck as follows:
        1. Title Slide
        2. Problem Statement
        3. Solution
        4. Market Opportunity
        5. Product/Service Demo
        6. Business Model
        7. Traction
        8. Go-to-Market Strategy
        9. Competitive Analysis
        10. Financial Projections
        11. Team Slide
        12. Funding Ask
        13. Closing Slide
        """
        logger.info("Sending request to OpenAI API for pitch deck generation.")
        
        pitch_deck_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that generates startup pitch decks. Using the prompt generate a well written detailed and if necessary quantified creative pitch deck"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
            top_p=0.95
        )

        pitch_deck_response_answer = pitch_deck_response.choices[0].message.content.strip()
        logger.info("Pitch Deck generated successfully.")
        return pitch_deck_response_answer
    except AttributeError as e:
        logger.error(f"AttributeError: {e}")
        return f"Failed to generate summary: AttributeError - {str(e)}"
    except Exception as e:
        logger.error(f"Exception: {e}")
        return f"Failed to generate summary: {str(e)}"
    