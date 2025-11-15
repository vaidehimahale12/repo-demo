# services/face_recognition_service.py
# This service handles the core logic of detecting faces in images and generating embeddings.

import numpy as np
from fastapi import UploadFile, HTTPException
import cv2
from insightface.app import FaceAnalysis

class FaceRecognitionService:
    """
    A singleton service class to encapsulate face detection and embedding generation.
    This approach ensures that the heavyweight `insightface` model is loaded only once.
    """
    def __init__(self):
        """
        Initializes the FaceAnalysis model from the insightface library.
        - `providers=['CPUExecutionProvider']`: Specifies that the model should run on the CPU.
        - `prepare(ctx_id=0, det_size=(640, 640))`: Prepares the model for inference.
        On the first run, this will download the necessary pre-trained models.
        """
        print("Initializing FaceAnalysis model...")
        self.app = FaceAnalysis(providers=['CPUExecutionProvider'])
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        print("FaceAnalysis model initialized.")

    async def get_face_embedding(self, file: UploadFile) -> np.ndarray:
        """
        Analyzes an uploaded image file to detect a face and generate a facial embedding.

        Args:
            file (UploadFile): The image file uploaded by the user.

        Returns:
            np.ndarray: A 512-dimensional NumPy array representing the face embedding.

        Raises:
            HTTPException (404): If no face is detected in the provided image.
        """
        # 1. Read the image file content from the UploadFile object.
        contents = await file.read()

        # 2. Convert the raw bytes into a NumPy array suitable for image processing.
        np_arr = np.frombuffer(contents, np.uint8)

        # 3. Decode the NumPy array into an OpenCV image format (BGR color order).
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # 4. Use the insightface model to perform face detection and analysis.
        #    The `get()` method returns a list of `Face` objects, each containing
        #    information like bounding box, landmarks, and the embedding vector.
        faces = self.app.get(img)

        # 5. Check if any faces were found in the image.
        if not faces:
            # If the list is empty, raise an error that the client can handle.
            raise HTTPException(status_code=404, detail="No face could be detected in the image.")

        # 6. Extract the normalized embedding from the first detected face.
        #    `normed_embedding` is a high-quality 512-d feature vector that represents the face.
        embedding = faces[0].normed_embedding

        return embedding

# --------------------------------------------------------------------------
# Singleton Instance
# --------------------------------------------------------------------------
# Create a single, globally accessible instance of the service.
# This ensures that the model is loaded only once when the application starts,
# improving performance by avoiding repeated initializations.
face_recognition_service = FaceRecognitionService()
