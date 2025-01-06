import json
import re
from typing import Dict
from app.models.health_check_model import HealthCheckInput
from app.services.query_service import summarize_with_llm


HEALTH_CHECK_DATA_PATH = "data/startup_health_check.json"

def load_health_check_data() -> Dict:
    """Load health check data from JSON file."""
    with open(HEALTH_CHECK_DATA_PATH, "r") as file:
        return json.load(file)

def extract_float_from_string(value: str) -> float:
    """Extract the first float number from a string."""
    match = re.search(r"[\d,.]+", value)
    if match:
        return float(match.group().replace(",", ""))
    raise ValueError(f"Could not extract a float from the string: {value}")

def compare_metrics(user_input: HealthCheckInput) -> Dict:
    """Compare user input with benchmark data."""
    data = load_health_check_data()
    stage_data = data.get("startup_health_checkup", {}).get(user_input.stage)
    
    if not stage_data:
        raise ValueError("Invalid stage provided. Please select a valid startup stage.")
    
    analysis = {}

    # Compare ROI
    roi_benchmark = stage_data["Profitability Ratios"]["ROI"].split("-")
    min_roi = extract_float_from_string(roi_benchmark[0])
    max_roi = extract_float_from_string(roi_benchmark[1]) if len(roi_benchmark) > 1 else min_roi
    analysis["ROI"] = (
        "Below Range" if user_input.ROI < min_roi else
        "Within Range" if min_roi <= user_input.ROI <= max_roi else
        "Above Range"
    )

    # Compare Gross Burn Rate
    gross_burn_range = stage_data["Burn Rate"]["Gross Burn Rate"].split("-")
    min_gross_burn = extract_float_from_string(gross_burn_range[0])
    max_gross_burn = extract_float_from_string(gross_burn_range[1])
    analysis["Gross Burn Rate"] = (
        "Below Range" if user_input.gross_burn_rate < min_gross_burn else
        "Within Range" if min_gross_burn <= user_input.gross_burn_rate <= max_gross_burn else
        "Above Range"
    )

    # Compare Net Burn Rate
    net_burn_range = stage_data["Burn Rate"]["Net Burn Rate"].split("-")
    min_net_burn = extract_float_from_string(net_burn_range[0])
    max_net_burn = extract_float_from_string(net_burn_range[1])
    analysis["Net Burn Rate"] = (
        "Below Range" if user_input.net_burn_rate < min_net_burn else
        "Within Range" if min_net_burn <= user_input.net_burn_rate <= max_net_burn else
        "Above Range"
    )

    # Compare CAC
    cac_range = stage_data["CAC and LTV"]["CAC"].split("-")
    min_cac = extract_float_from_string(cac_range[0])
    max_cac = extract_float_from_string(cac_range[1])
    analysis["CAC"] = (
        "Below Range" if user_input.CAC < min_cac else
        "Within Range" if min_cac <= user_input.CAC <= max_cac else
        "Above Range"
    )

    # Compare MRR
    mrr_range = stage_data["Revenue Growth"]["MRR"].split("-")
    min_mrr = extract_float_from_string(mrr_range[0])
    max_mrr = extract_float_from_string(mrr_range[1])
    analysis["MRR"] = (
        "Below Range" if user_input.MRR < min_mrr else
        "Within Range" if min_mrr <= user_input.MRR <= max_mrr else
        "Above Range"
    )

    # Pass to LLM for summarization
    llm_summary = summarize_with_llm(user_input.stage, analysis)

    return {
        "analysis": analysis,
        "summary": llm_summary
    }

