from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np

app = FastAPI()

total_people = 0

@app.get("/")
def home():
    return {"message": "AI Camera Server Running"}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    global total_people
    
    image_bytes = await file.read()
    np_arr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # simple detection placeholder
    persons = 1

    total_people += persons

    return {
        "persons": persons,
        "total_people_today": total_people
    }
