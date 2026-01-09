from ultralytics import YOLO
 
 #load the finetuned model
model = YOLO("model/best.pt")

 # Get the class names
Cname = model.names

 #function to take single image and return detections
def predict(image):
    results = model(image)
    detections =[]
    #Loop through the each detected  bounding box
    for box in results[0].boxes:
        detections.append({
        "class_name": Cname[int(box.cls)],
        "confidence": box.conf.item(),
        "bbox": [
            float(box.xyxy[0][0]),
            float(box.xyxy[0][1]),
            float(box.xyxy[0][2]),
            float(box.xyxy[0][3])
        ]
    })
    return detections
