from pydantic import BaseModel, Field

class HealthCheckInput(BaseModel):
    stage: str = Field(..., description="Startup Stage (e.g., Pre-seed, Series A, Series B)")
    ROI: float = Field(..., description="Return on Investment percentage (e.g., 5.0)")
    gross_burn_rate: float = Field(..., description="Gross Burn Rate in USD (e.g., 50000)")
    net_burn_rate: float = Field(..., description="Net Burn Rate in USD (e.g., 30000)")
    CAC: float = Field(..., description="Customer Acquisition Cost in USD (e.g., 1000)")
    MRR: float = Field(..., description="Monthly Recurring Revenue in USD (e.g., 20000)")
