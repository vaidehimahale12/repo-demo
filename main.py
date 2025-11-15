# main.py
# This script initializes and configures the FastAPI application.

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import character_routes, upload_routes

# --------------------------------------------------------------------------
# FastAPI App Initialization
# --------------------------------------------------------------------------
# Create the main FastAPI application instance with metadata for documentation.
app = FastAPI(
    title="Marvel Look-Alike API",
    description="An API that uses facial recognition to find your Marvel character look-alike. Upload a photo and see which hero you resemble!",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
)

# --------------------------------------------------------------------------
# Middleware Configuration
# --------------------------------------------------------------------------
# Set up CORS (Cross-Origin Resource Sharing) to allow the frontend
# to communicate with this backend.
# For development, we allow all origins ("*"). In a production environment,
# this should be restricted to the specific frontend domain.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all standard HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --------------------------------------------------------------------------
# API Routers
# --------------------------------------------------------------------------
# Include the routers for different parts of the API.
# This keeps the code modular and organized.
app.include_router(upload_routes.router, prefix="/api", tags=["Face Recognition"])
app.include_router(character_routes.router, prefix="/api", tags=["Characters"])

# --------------------------------------------------------------------------
# Root Endpoint & Health Check
# --------------------------------------------------------------------------
@app.get("/", tags=["Root"])
async def read_root():
    """
    A welcome message for the root URL.
    """
    return {"message": "Welcome to the Marvel Look-Alike API!"}

@app.get("/health-check", tags=["Health Check"])
async def health_check():
    """
    A simple endpoint to verify that the API is running and responsive.
    """
    return {"status": "ok", "message": "API is healthy"}

# --------------------------------------------------------------------------
# Application Startup
# --------------------------------------------------------------------------
# The entry point for running the application.
# `uvicorn.run()` starts the server. This block is executed when the script
# is run directly (e.g., `python main.py`).
# For production, it's recommended to use a process manager like Gunicorn.
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
