#importing FastAPI framework and required libraries for image processing
from fastapi import FastAPI, UploadFile, File, HTTPException
import numpy as np
import cv2
import redis
import json
import os

from app.schemas import PredictionResponse
from model.model_run import predict

#creating FastAPI application
app = FastAPI(title="Bangladeshi Taka Note and Coin Detection API")

#Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

#connecting to Redis server
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

#Defining a GET endpoint for health check
@app.get("/", tags=["Health Check"])
def health_check():
    return {"message": "API is up and running"}

#Defining a POST endpoint for image prediction
@app.post("/predict/", response_model=PredictionResponse)
async def predict_image(image: UploadFile = File(...)):

    #checking if the uploaded file is an image
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Only image (jpeg, png) files are allowed."
        )

    #using image filename as Redis cache key
    redis_key = image.filename

    #checking if result already exists in Redis cache
    try:
        cached_result = redis_client.get(redis_key)
        if cached_result:
            return json.loads(cached_result)
    except Exception:
        #if Redis is not available, continue without cache
        pass

    #reading the uploaded image file
    image_data = await image.read()

    #converting image bytes to numpy array
    img_arr = np.frombuffer(image_data, np.uint8)

    #decoding numpy array to OpenCV image
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

    #checking if image decoding was successful
    if img is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file."
        )

    #running finetuned YOLOv11 model inference
    results = predict(img)

    #preparing final response in JSON format
    response = {
        "filename": image.filename,
        "detections": results
    }

    #storing prediction result in Redis for future requests
    try:
        redis_client.set(redis_key, json.dumps(response), ex=3600)
    except Exception:
        pass

    #returning the prediction response
    return response
