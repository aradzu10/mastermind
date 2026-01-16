from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import games
import os

app = FastAPI(
    title="Mastermind API",
    description="Full-stack Mastermind game with AI opponents and multiplayer",
    version="2.0.0"
)

# CORS middleware
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(games.router)


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Mastermind API is running"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Mastermind API",
        "version": "2.0.0",
        "docs": "/docs"
    }
