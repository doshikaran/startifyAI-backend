from fastapi import FastAPI
from app.config import settings
from app.api.routes import router
from app.api.routes import router as health_check_router
from app.api.routes import router as pitch_deck

from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="StartifyAI"
)

# Include Routes
app.include_router(router)
app.include_router(health_check_router, prefix="/api", tags=["Health Check"])
app.include_router(pitch_deck, prefix="/api", tags=["Pitch Deck"])

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Startup Copilot API"}