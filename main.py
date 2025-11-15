# main.py
# This script initializes and configures the FastAPI application.

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------------
# Static Files Configuration
# --------------------------------------------------------------------------
# Mount the 'frontend' directory to serve static files like HTML, CSS, and JS.
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


# --------------------------------------------------------------------------
# API Routers
# --------------------------------------------------------------------------
# Include the routers for different parts of the API.
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
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
