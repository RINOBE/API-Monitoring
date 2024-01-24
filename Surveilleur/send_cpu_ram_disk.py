import asyncio
import websockets
import httpx  # Assurez-vous d'installer cette bibliothèque avec 'pip install httpx'
import psutil
import json
import platform
import speedtest
from config import client_id,client_secret,server_address,server_port
async def get_access_token():
    token_url = f"http://{server_address}:{server_port}/token"  # Remplacez cette URL par l'URL de votre endpoint token
    async with httpx.AsyncClient() as client:
        data = {
            "username": client_id,
            "password": client_secret
        }

        response = await client.post(token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            return access_token
        else:
            print(f"Échec de l'obtention du token. Statut de réponse : {response.status_code}")
            return None
async def send_system_info(websocket):
    while True:
        cpu_percent = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        system_info = {"cpu_usage": cpu_percent,"ram_available": round(ram.available/(1024**3),2),"ram_total": round(ram.total/(1024**3),2),"disk_available": round(disk.free/(1024**3),2),"disk_total": round(disk.total/(1024**3),2)}
        await websocket.send(json.dumps(system_info))
        await asyncio.sleep(10)  # Envoi toutes les 10 secondes
async def main():
    access_token = await get_access_token()
    if access_token:
        uri = f"ws://{server_address}:{server_port}/crd/?token=f{access_token}"  # Remplacez cette URL par l'URL de votre WebSocket
        headers = {"Authorization": f"Bearer {access_token}"}
        async with websockets.connect(uri,extra_headers=headers,ping_interval=None) as websocket:
            while True:
                await send_system_info(websocket)
            
if __name__ == "__main__":
    asyncio.run(main())
    
