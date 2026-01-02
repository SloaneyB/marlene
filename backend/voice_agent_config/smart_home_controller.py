import asyncio
import requests

async def control_smart_home(parameters):
    await asyncio.to_thread(
        requests.get,
        "https://api-v2.voicemonkey.io/trigger?token=6c2b56bd90622670b32fb308d4c81568_cd6fd565a2fc264d565316b4b40118d2&device=toggle-the-living-room-lamp"
    )
    print("Conrolling smart home now!!!@@!!@@!!")
