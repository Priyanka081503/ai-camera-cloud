from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            # broadcast to all connected dashboards
            for client in clients:
                await client.send_text(data)

    except:
        clients.remove(websocket)


@app.get("/")
def home():
    return {"status": "AI camera cloud running"}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    html = """
    <html>
    <head>
        <title>AI Camera Dashboard</title>
    </head>

    <body>

    <h1>Live AI Camera</h1>

    <img id="video" width="640"/>

    <script>

    const ws = new WebSocket("wss://ai-camera-cloud-3.onrender.com/ws");

    ws.onmessage = function(event){
        document.getElementById("video").src =
        "data:image/jpeg;base64," + event.data;
    }

    </script>

    </body>
    </html>
    """

    return html
