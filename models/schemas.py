# models/schemas.py
# This file defines the Pydantic models used for data validation, serialization,
# and documentation in the FastAPI application.

from pydantic import BaseModel, Field
from typing import List

# --------------------------------------------------------------------------
# API Response Schemas
# --------------------------------------------------------------------------
# These models define the structure of the data sent back to the client.

class CharacterMatch(BaseModel):
    """
    Represents the successful result of a character look-alike search.
    This is the main response model for the /upload-photo endpoint.
    """
    character_name: str = Field(..., example="Captain America", description="The name of the matched Marvel character.")
    similarity_score: float = Field(..., gt=0, le=1, example=0.87, description="The cosine similarity score, where 1.0 is a perfect match.")
    meme_text: str = Field(..., example="On your left!", description="A generated meme caption (placeholder for now).")
    image_url: str = Field(..., example="https://path/to/character_image.jpg", description="A URL to the matched character's image.")

    class Config:
        # Provides example data for API documentation.
        schema_extra = {
            "example": {
                "character_name": "Thor",
                "similarity_score": 0.92,
                "meme_text": "This human is worthy!",
                "image_url": "https://example.com/images/thor.jpg"
            }
        }

class CharacterInfo(BaseModel):
    """
    A simplified model representing basic information about a single character.
    Used in the /get-characters endpoint.
    """
    name: str = Field(..., example="Iron Man", description="The name of the character.")
    image_url: str = Field(..., example="https://path/to/iron_man.jpg", description="A URL to the character's image.")

    class Config:
        schema_extra = {
            "example": {
                "name": "Black Widow",
                "image_url": "https://example.com/images/black_widow.jpg"
            }
        }

class ErrorResponse(BaseModel):
    """
    A standard structure for returning error messages from the API.
    This is used in the `responses` dictionary of endpoint decorators.
    """
    detail: str = Field(..., example="No face could be detected in the image.", description="A clear, user-friendly error message.")

# --------------------------------------------------------------------------
# API Request Schemas
# --------------------------------------------------------------------------
# Currently, no JSON body request models are needed since the primary input
# is a file upload. This section could be expanded if endpoints that
# accept structured JSON data are added in the future.
