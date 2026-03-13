from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np

app = FastAPI()

latest_result = {"persons": 0}

@app.get("/")
def home():
    return {"message": "AI Camera Server Running"}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):

    global latest_result

    image_bytes = await file.read()

    npimg = np.frombuffer(image_bytes, np.uint8)

    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Dummy detection for now
    persons = 1

    latest_result["persons"] = persons

    return latest_result


@app.get("/latest")
def latest():
    return latest_result
