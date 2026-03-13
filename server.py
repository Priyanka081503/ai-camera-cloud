from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
from ultralytics import YOLO

app = FastAPI()

model = YOLO("yolov8n.pt")

latest_result = {"persons":0}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):

    global latest_result

    image_bytes = await file.read()

    npimg = np.frombuffer(image_bytes, np.uint8)

    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    results = model(frame)

    persons = 0

    for r in results:
        for box in r.boxes:
            if int(box.cls) == 0:
                persons += 1

    latest_result["persons"] = persons

    return latest_result


@app.get("/latest")
def latest():

    return latest_result
