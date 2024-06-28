
from fastapi import FastAPI, HTTPException,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import httpx  # Asynchronous HTTP client
from pydantic import BaseModel

class ImageData(BaseModel):
    imageString: str

from detectionModel import getBoundingBox

app = FastAPI()
                                                                                                                                                                                                                                                                                                                                                                                 
origins = [BASE_URL,"http://localhost:3000/scene/new"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


    
@app.post("/detect/")
async def detect(image_data:ImageData):
    imageUrl = image_data.imageString
    print(imageUrl)
    if not imageUrl:
        raise HTTPException(status_code=400, detail="No image URL provided.")

    try:
        # Asynchronously fetch the image from the URL
        async with httpx.AsyncClient() as client:
            response = await client.get(imageUrl)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch image.")

        # Convert the bytes to a NumPy array and decode the image
        nparr = np.frombuffer(response.content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Predict and get bounding boxes
        bboxesObjects = await getBoundingBox(img)
        
        # Ensure all coordinates are in list format for JSON serialization
        for obj in bboxesObjects:
            if isinstance(obj['coords'], np.ndarray):
                obj['coords'] = obj['coords'].tolist()  # Convert ndarray to list if not already done

        return JSONResponse(content=bboxesObjects)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))