#Data validation tasks using Pydantic models
from pydantic import BaseModel
from typing import List

# Pydantic model for individual detection
class Detection(BaseModel):
    class_name: str
    confidence: float
    bbox: List[float]


# Pydantic model for prediction response in API responses format
class PredictionResponse(BaseModel):
    filename: str
    detections: List[Detection]