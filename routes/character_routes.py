# routes/character_routes.py
# This file defines the API routes related to character information.

from fastapi import APIRouter
from typing import List
from models.schemas import CharacterInfo
from services.vector_db_service import vector_db_service

# Create an APIRouter instance for organizing routes.
router = APIRouter()

# --------------------------------------------------------------------------
# Endpoint: /get-characters
# --------------------------------------------------------------------------
@router.get(
    "/get-characters",
    response_model=List[CharacterInfo],
    summary="Get a list of all available Marvel characters",
    description=(
        "Retrieves a complete list of all Marvel characters whose embeddings are stored in the vector database. "
        "This endpoint is useful for frontend displays, such as a gallery of available characters."
    ),
)
async def get_characters():
    """
    Handles the request to get all available characters.

    - It accesses the singleton `vector_db_service` to get the metadata.
    - It then formats this metadata into a list of `CharacterInfo` objects.
    - FastAPI automatically handles the JSON serialization of this response.
    """
    # 1. Access the metadata loaded by the VectorDBService.
    #    This metadata is a list of dictionaries, where each dictionary
    #    contains details about a character.
    characters_metadata = vector_db_service.metadata

    # 2. Use a list comprehension to transform the metadata into the desired
    #    Pydantic response model format (`CharacterInfo`).
    #    This ensures the response is validated and conforms to the defined schema.
    return [
        CharacterInfo(name=char["character_name"], image_url=char["image_url"])
        for char in characters_metadata
    ]
