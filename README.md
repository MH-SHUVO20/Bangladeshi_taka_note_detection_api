## Deployment of Bangladeshi Taka Note Detection Model Using REST API & Docker

Deploy a YOLOv11-based detector for Bangladeshi taka notes and coins behind a FastAPI REST API. The service accepts an image, runs inference, and returns denomination names with confidence scores and bounding boxes. Docker and Docker Compose provide a one-command setup with Redis caching.

---

### Model Details
- Model: YOLOv11 (Ultralytics)
- Task: Object detection for Bangladeshi notes and coins
- Weights: `best.pt` (from Phase-1)

---

### Project Structure
```
Bangladeshi_taka_note_detection_api/
├── app/
│   ├── main.py          # FastAPI application
│   └── schemas.py       # Pydantic response models
├── model/
│   ├── best.pt          # Trained YOLOv11 weights
│   └── model_run.py     # Model loading & inference logic
├── test_images/         # Images used for API testing
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

Key files: [app/main.py](app/main.py), [app/schemas.py](app/schemas.py), [model/model_run.py](model/model_run.py), [model/best.pt](model/best.pt), [docker-compose.yml](docker-compose.yml), [Dockerfile](Dockerfile).

---

### REST API Endpoints
- GET `/` — health check
  - Response:
    ```json
    {"message": "API is up and running"}
    ```
- POST `/predict/` — form-data upload with `image` (jpeg/png)
  - Response example:
    ```json
    {
      "filename": "1000_tk (152).jpg",
      "detections": [
        {
          "class_name": "1000_Tk",
          "confidence": 0.95,
          "bbox": [x1, y1, x2, y2]
        }
      ]
    }
    ```

---

### Quickstart (Docker Compose)
1) Build and run API + Redis:
```
docker-compose up --build
```
2) API base: http://127.0.0.1:5000
3) Swagger UI: http://127.0.0.1:5000/docs

Test with curl:
```
curl.exe -X POST "http://127.0.0.1:5000/predict/" -H "accept: application/json" -F "image=@test_images/1000_tk (152).jpg"
```

Stop services: `docker-compose down`.

---

### Local Run (no Docker)
1) Create and activate a virtual environment.
2) Install dependencies:
```
pip install -r requirements.txt
```
3) Start the API:
```
uvicorn app.main:app --host 0.0.0.0 --port 5000
```
4) Open http://127.0.0.1:5000/docs to try requests.

Set `REDIS_HOST` and `REDIS_PORT` if you have Redis available; caching is skipped gracefully if unavailable.

---

### Requirements
- FastAPI
- Uvicorn
- Ultralytics
- OpenCV
- NumPy
- Redis
- python-multipart
- Pydantic

Full list is in [requirements.txt](requirements.txt).

---

### Documentation & Assignment Notes
- Detailed discussion, screenshots, curl runs, Docker logs, and accuracy notes are in the accompanying Google Doc.
- Covers: model integration, REST API development, API testing via curl, Dockerized deployment, and documentation.

---

### Author
Md. Mehedi Hasan Shuvo
BSc in Computer Science & Engineering, Bangladesh

