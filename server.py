from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
from fastapi.responses import HTMLResponse

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
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    html = f"""
    <html>
    <head>
        <title>AI Camera Dashboard</title>
    </head>
    <body>
        <h1>AI Camera Analytics</h1>
        <p>Total People Detected Today: {total_people}</p>
    </body>
    </html>
    """
    return html
