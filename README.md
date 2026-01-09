### Bangladeshi Taka Note Detection API

Production-ready FastAPI service exposing a YOLOv11 model for Bangladeshi taka note and coin detection. Upload an image, get back denomination labels, confidence scores, and bounding boxes. Docker Compose bundles the API with Redis for response caching.

---

### Highlights
- YOLOv11 model weights included at [model/best.pt](model/best.pt); no extra download needed
- FastAPI with Swagger UI for interactive testing
- Redis-backed response caching (optional locally, enabled in Compose)
- Single-command container startup via [docker-compose.yml](docker-compose.yml)

---

### Technology Stack
- FastAPI + Uvicorn
- Ultralytics YOLOv11
- Redis
- Docker / Docker Compose
- OpenCV, NumPy, python-multipart, Pydantic

---

### System Architecture
1) Client uploads an image to `/predict/`.
2) [app/main.py](app/main.py) validates content type, decodes bytes, and checks Redis cache.
3) [model/model_run.py](model/model_run.py) loads YOLOv11 once and performs inference.
4) Detections are serialized using [app/schemas.py](app/schemas.py) and cached by filename (if Redis is available).

---

### Run It
**Prerequisites:** Docker + Docker Compose (recommended) or Python 3.10+ for local.

#### Step-by-Step (Windows + Docker Desktop)
1) Install Docker Desktop and restart if prompted.
  - Verify: `docker --version` and `docker-compose --version`
2) Open PowerShell in the project folder.
3) Build and start services:
  ```bash
  docker-compose up --build
  ```
4) Wait until the API reports it is running on port 5000.
5) Check health:
  ```bash
  curl.exe http://127.0.0.1:5000/
  ```
6) Predict with a sample image:
  ```bash
  curl.exe -X POST \
    http://127.0.0.1:5000/predict/ \
    -H "accept: application/json" \
    -F "image=@test_images/1000_tk (152).jpg"
  ```
7) Stop services when done:
  ```bash
  docker-compose down
  ```

#### Option A: Docker Compose
1) Build and start API + Redis:
```
docker-compose up --build
```
2) API base: http://127.0.0.1:5000
3) Swagger UI: http://127.0.0.1:5000/docs
4) Sample request:
```
curl -X POST \
  http://127.0.0.1:5000/predict/ \
  -H "accept: application/json" \
  -F "image=@test_images/1000_tk (152).jpg"
```
Stop services when done: `docker-compose down`.

#### Option B: Local (no Docker)
1) Create and activate a virtual environment.
2) Install dependencies:
```
pip install -r requirements.txt
```
3) Start the API:
```
uvicorn app.main:app --host 0.0.0.0 --port 5000
```
4) Open http://127.0.0.1:5000/docs to exercise endpoints.

Set `REDIS_HOST` and `REDIS_PORT` if you have Redis running; the API skips caching if Redis is unreachable.

---

### API Reference
- GET `/` — health check
  - Response: `{"message": "API is up and running"}`
- POST `/predict/` — form-data upload with field `image` (jpeg/png)
  - Response example:
    ```json
    {
      "filename": "1000_tk (152).jpg",
      "detections": [
        {
          "class_name": "1000_Tk",
          "confidence": 0.95,
          "bbox": [2.332881450653076,2.3923535346984863,1131.0,2585.786376953125]
        }
      ]
    }
    ```

Swagger UI and OpenAPI schema are available at `/docs` and `/openapi.json`.

---

### Configuration
- `REDIS_HOST` (default `localhost` locally; `redis` in Docker Compose)
- `REDIS_PORT` (default `6379`)

These are injected automatically in Docker Compose so the API connects to the bundled Redis service.

---

### Project Layout
```
Bangladeshi_taka_note_detection_api/
├── app/
│   ├── main.py          # FastAPI application and Redis caching
│   └── schemas.py       # Pydantic response models
├── model/
│   ├── best.pt          # Trained YOLOv11 weights
│   └── model_run.py     # Model loading & inference logic
├── test_images/         # Sample images for manual testing
├── Dockerfile           # API container image
├── docker-compose.yml   # API + Redis services
├── requirements.txt
└── README.md
```

---

### Notes
- Rebuild the image after dependency or model changes: `docker-compose build`.
- Use the provided `test_images` to sanity-check predictions before integrating upstream.

- On Windows, prefer `curl.exe` in PowerShell to avoid alias conflicts.
- If a path contains spaces, wrap the entire `-F` value in quotes as shown above.

---

### Prediction Accuracy
- Typical detections achieve high confidence on real-world images.
- Bounding boxes remain stable across varied lighting and backgrounds.
- Results depend on input quality; clear, well-lit images perform best.


---

### Author
Md. Mehedi Hasan Shuvo — BSc in Computer Science & Engineering, Bangladesh

