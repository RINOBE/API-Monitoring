import asyncio
import websockets
import httpx 
import json
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
async def send_speed_test_results(websocket):
    while True:
        st = speedtest.Speedtest()
        download_speed = round(st.download() / 10**6,2)  # Convertir en Mbps
        upload_speed = round((st.upload() / 10**6),2)  # Convertir en Mbps
        speed_test_results = {"download_speed": download_speed,"upload_speed": upload_speed}
        await websocket.send(json.dumps(speed_test_results))
        await asyncio.sleep(30)
async def main():
    access_token = await get_access_token()
    if access_token:
        uri = f"ws://{server_address}:{server_port}/network/?token=f{access_token}"  # Remplacez cette URL par l'URL de votre WebSocket
        headers = {"Authorization": f"Bearer {access_token}"}
        async with websockets.connect(uri,extra_headers=headers,ping_interval=None) as websocket:
            while True:   
                await send_speed_test_results(websocket)
                await asyncio.sleep(2)
            
if __name__ == "__main__":
    asyncio.run(main())
    
