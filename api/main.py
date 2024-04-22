from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
import cv2

from detectionModel import getBoundingBox , box_to_dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins=[
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows the origins listed in origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.post("/detect/")
async def detect(image: UploadFile):
    # Ensure the file is an image
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        # Read the image file as bytes
        content = await image.read()
        
        # Convert the bytes to a NumPy array of type uint8
        nparr = np.frombuffer(content, np.uint8)
        
        # Decode the image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Now `img` is a NumPy array that can be used with OpenCV and other libraries
        # Predict and get bounding boxes
        bboxesObjects = await getBoundingBox(img)
        # bboxes=[box_to_dict(box) for box in bboxesObjects]

        return JSONResponse(content=bboxesObjects)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))