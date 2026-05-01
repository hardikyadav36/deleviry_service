# import asyncio
# import websockets
# import json
# import random
# import os
# from dotenv import load_dotenv

# load_dotenv()

# async def send_location():
#     # Use 'app' as hostname when running in Docker, 'localhost' for local development
#     host = os.getenv("BACKEND_HOST", "localhost")
#     port = os.getenv("APP_PORT")
#     uri = f"ws://{host}:{port}/ws/1"
#     uri = "ws://backend:8000/ws/1"

#     async with websockets.connect(uri) as websocket:
#         lat, lng = 28.6139, 77.2090

#         while True:
#             lat += random.uniform(-0.0005, 0.0005)
#             lng += random.uniform(-0.0005, 0.0005)

#             data = {
#                 "latitude": lat,
#                 "longitude": lng
#             }

#             await websocket.send(json.dumps(data))
#             print("Sent:", data)

#             await asyncio.sleep(2)
# #
# asyncio.run(send_location())


import asyncio
import websockets
import json
import random
import os
from dotenv import load_dotenv

load_dotenv()

async def send_location():
    host = os.getenv("BACKEND_HOST", "backend")  # default docker service
    port = os.getenv("APP_PORT", "8000")

    uri = f"ws://{host}:{port}/ws/1"

    lat, lng = 28.6139, 77.2090  # initial location

    while True:  # 🔥 retry loop
        try:
            print(f"Connecting to {uri}...")
            async with websockets.connect(uri) as websocket:
                print("✅ Connected to backend")

                while True:
                    lat += random.uniform(-0.0005, 0.0005)
                    lng += random.uniform(-0.0005, 0.0005)

                    data = {
                        "latitude": lat,
                        "longitude": lng
                    }

                    await websocket.send(json.dumps(data))
                    print("📍 Sent:", data)

                    await asyncio.sleep(2)

        except Exception as e:
            print(f"❌ Connection error: {e}")
            print("🔁 Retrying in 3 seconds...\n")
            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(send_location())