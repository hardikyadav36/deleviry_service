import asyncio
import websockets
import json
import random
import os
from dotenv import load_dotenv

load_dotenv()

async def send_location():
    # Use 'app' as hostname when running in Docker, 'localhost' for local development
    host = os.getenv("BACKEND_HOST", "localhost")
    port = os.getenv("APP_PORT")
    uri = f"ws://{host}:{port}/ws/1"

    async with websockets.connect(uri) as websocket:
        lat, lng = 28.6139, 77.2090

        while True:
            lat += random.uniform(-0.0005, 0.0005)
            lng += random.uniform(-0.0005, 0.0005)

            data = {
                "latitude": lat,
                "longitude": lng
            }

            await websocket.send(json.dumps(data))
            print("Sent:", data)

            await asyncio.sleep(2)

asyncio.run(send_location())