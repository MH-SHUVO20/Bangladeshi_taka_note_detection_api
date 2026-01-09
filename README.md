# Deployment of Bangladeshi Taka Note Detection Model Using REST API & Docker

## Project Title (Phase-2)
Deployment of Bangladeshi Taka Note Detection Model Using REST API & Docker

---

## Project Overview
This project focuses on deploying a trained **YOLOv11-based Bangladeshi Taka Note and Coin Detection model** using a **REST API** and **Docker**.  
The system allows users to upload an image and receive detected currency denominations along with confidence scores and bounding box coordinates.

The project is developed using **FastAPI**, **Redis** for caching, and **Docker/Docker Compose** for containerization.

---

## Folder Structure
Bangladeshi_taka_note_detection_api/
│
├── app/
│ ├── main.py
│ └── schemas.py
│
├── model/
│ ├── best.pt
│ └── model_run.py
│
├── test_images/
│ ├── sample Bangladeshi currency images for testing
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
---

## Task 1: Model Integration & Inference Pipeline
- The trained YOLOv11 model weights (`best.pt`) from Phase-1 are loaded.
- A single image inference pipeline is implemented in `model/model_run.py`.
- The pipeline:
  - Accepts a single image
  - Performs object detection
  - Returns detected class names, confidence scores, and bounding box coordinates
- Inference was tested using sample images from the `test_images` folder.

---

## Task 2: REST API Development
The REST API is developed using FastAPI.

### API Endpoints

#### Health Check
GET /

Response:
```json
{
  "message": "API is up and running"
}

Prediction Endpoint
POST /predict/


Input

Image file (JPEG or PNG)

Output

{
  "filename": "image.jpg",
  "detections": [
    {
      "class_name": "5_Tk_Coin",
      "confidence": 0.96,
      "bbox": [x1, y1, x2, y2]
    }
  ]
}

Task 3: API Testing & Validation

The API was tested using Swagger UI (/docs) and Postman.

At least 5 different images from the test_images folder were used.

The prediction results were verified for correctness and response format.

Task 4: Dockerization of the Application

The application is containerized using Docker.

Docker Compose is used to run:

FastAPI application

Redis cache service

Run Using Docker
docker-compose up --build

Access API

API root: http://127.0.0.1:5000/

Swagger UI: http://127.0.0.1:5000/docs

Task 5: Documentation

Code is well-structured and commented.

Project follows Docker and REST API best practices.

This README provides full usage instructions.

Technologies Used

Python 3.11

FastAPI

YOLOv11 (Ultralytics)

OpenCV

Redis

Docker & Docker Compose

Author

Md. Mehedi Hasan Shuvo
Department of CSE
American International University–Bangladesh (AIUB)

