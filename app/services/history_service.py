from app.utils.db import get_collection
from datetime import datetime
from typing import List, Dict
import logging


def add_history_entry(user_id: str, entry_type: str, input_data: Dict, output: str):
    """
    Add a history entry to MongoDB.
    """
    try:
        history_collection = get_collection("history")
        history_collection.insert_one({
            "user_id": user_id,
            "type": entry_type,
            "input": input_data,
            "output": output,
            "timestamp": datetime.utcnow()
        })
        logging.info("History entry added successfully.")
    except Exception as e:
        logging.error(f"Failed to add history entry: {e}")
        raise e


def get_user_history(user_id: str) -> List[Dict]:
    """
    Retrieve history entries for a specific user.
    """
    try:
        history_collection = get_collection("history")
        results = history_collection.find(
            {"user_id": user_id},
            {"_id": 0}  # Exclude MongoDB's _id field
        ).sort("timestamp", -1)

        history_list = list(results)

        if not history_list:
            logging.info(f"No history found for user: {user_id}")
            return []

        logging.info("User history fetched successfully.")
        return history_list
    except Exception as e:
        logging.error(f"Failed to fetch user history: {e}")
        raise e
