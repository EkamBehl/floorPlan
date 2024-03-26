
from ultralytics import YOLO
import json
import cv2
import numpy as np

async def getBoundingBox(image: np.ndarray) -> list[dict]:
    # Load a pretrained YOLOv8 model
    model = YOLO('./last.pt')
    device = "cpu"
    
    # Run inference on the image
    results = model.predict(image, conf=0.4, device=device)
    
    jsonArray = []
    boxes = results[0].cpu().numpy().boxes
    names = results[0].cpu().numpy().names  # Assuming this is correct

    for i in range(len(boxes.cls)):
        jsonObject = {
            'class': names[int(boxes.cls[i])],  # Use class names directly
            'confidence': float(boxes.conf[i]),
            'coords': boxes.xyxy[i].tolist()  # Convert ndarray to list
        }
        
        jsonArray.append(jsonObject)
    
    print("jsonArray: ", jsonArray)
    return jsonArray
def box_to_dict(box):
    # Convert a single Box object to a dictionary
    # This is a placeholder. Adapt the attributes access according to your Box object's structure
    return {
        "x": box.x,
        "y": box.y,
        "width": box.w,
        "height": box.height,
        "confidence": box.conf,
        "class": box.cls  # Assuming `class_name` is an attribute; adjust as necessary
    }