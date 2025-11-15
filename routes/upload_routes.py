# routes/upload_routes.py
# Defines the API endpoint for uploading a photo for face recognition.

from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import CharacterMatch, ErrorResponse
from services.face_recognition_service import face_recognition_service
from services.vector_db_service import vector_db_service

# Create an APIRouter instance for organizing routes.
router = APIRouter()

# --------------------------------------------------------------------------
# Endpoint: /upload-photo
# --------------------------------------------------------------------------
@router.post(
    "/upload-photo",
    response_model=CharacterMatch,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid image format submitted"},
        404: {"model": ErrorResponse, "description": "No face was detected in the image"},
        500: {"model": ErrorResponse, "description": "An unexpected internal server error occurred"},
    },
    summary="Upload a photo to find your Marvel look-alike",
    description=(
        "This is the main endpoint of the application. It accepts an image file (JPEG or PNG), "
        "detects a face, generates a facial embedding, and searches the vector database "
        "to find the most similar Marvel character."
    ),
)
async def upload_photo(file: UploadFile = File(..., description="An image file (JPEG or PNG format).")):
    """
    Handles the image upload, processing, and matching logic.

    - **file**: The uploaded image, injected by FastAPI's `File` dependency.
    """
    # 1. --- Input Validation ---
    #    Although the frontend should enforce this, we validate the content type on the
    #    backend as a security best practice.
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid image format. Only JPEG or PNG files are accepted.",
        )

    try:
        # 2. --- Face Embedding Generation ---
        #    Call the face recognition service to get the embedding vector for the user's face.
        #    This is an async operation because reading the file is I/O-bound.
        user_embedding = await face_recognition_service.get_face_embedding(file)

        # 3. --- Vector Database Search ---
        #    Use the generated embedding to find the closest match in the FAISS index.
        #    This returns the character's metadata and the similarity score.
        matched_character, similarity = vector_db_service.find_closest_match(user_embedding)

        # 4. --- Response Creation ---
        #    Construct the response using the `CharacterMatch` Pydantic model.
        #    This ensures the output is structured and validated.
        response = CharacterMatch(
            character_name=matched_character["character_name"],
            similarity_score=similarity,
            meme_text="This is a placeholder for the meme generation logic.",  # Placeholder for Prompt #3
            image_url=matched_character["image_url"],
        )

        return response

    except HTTPException as e:
        # 5. --- Specific Error Handling ---
        #    If a known HTTPException was raised (e.g., 'No face found' from the service),
        #    re-raise it so FastAPI can send the appropriate client error response.
        raise e
    except Exception as e:
        # 6. --- General Error Handling ---
        #    Catch any other unexpected errors during the process.
        #    Log the error for debugging and return a generic 500 server error
        #    to avoid exposing internal implementation details.
        print(f"An unexpected error occurred during photo upload processing: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
