import asyncio
import psutil
import websockets
import httpx
import os
import datetime
import json
import subprocess
from config import client_id,client_secret,server_address,server_port
def get_internet_ip():
    internet_interface = None
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == 2:  # Recherche d'adresses IPv4
                if not addr.address.startswith('127.'):
                    internet_interface = interface
                    break
        if internet_interface:
            break

    if internet_interface:
        return psutil.net_if_addrs()[internet_interface][0].address
    else:
        return "Adresse IP non trouvée"
ip_address=get_internet_ip()
async def get_access_token():
    token_url = f"http://{server_address}:{server_port}/token"  # Remplacez cette URL par l'URL de votre endpoint token
    async with httpx.AsyncClient() as client:
        data = {"username": client_id, "password": client_secret}

        response = await client.post(token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            return access_token
        else:
            print(f"Échec de l'obtention du token. Statut de réponse : {response.status_code}")
            return None

async def send_command_history(websocket):
    #dd Lire le contenu du fichier d'historique de Bash
    # Commande Bash que vous souhaitez exécuter
    bash_command = "/home/rino/python_code/affiche_history_all.sh"
    # Exécutez la commande Bash
    completed_process = subprocess.run(bash_command,stdout=subprocess.PIPE,     stderr=subprocess.PIPE, text=True)
    # Récupérez la sortie de la commande
    output = completed_process.stdout

    # Chemin vers le fichier d'historique formaté
    history_output= output.split("\n")
    # Lire le fichier d'historique
    history_data = []
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for line in history_output:
        if line!="":
            line_split= line.split(" ",1)
            history_data.append({"user": line_split[0], "command": line_split[1],"created_at":current_datetime})
    
    for history in history_data:
        history_json=json.dumps(history)
        await websocket.send(history_json)  
async def main():
    access_token = await get_access_token()
    if access_token:
        uri = f"ws://{server_address}:{server_port}/history/?token={access_token}"  # Remplacez cette URL par l'URL de votre WebSocket
        headers = {"Authorization": f"Bearer {access_token}"}  
        async with websockets.connect(uri, extra_headers=headers,ping_interval=None) as websocket:
            while True:
                await send_command_history(websocket)
                await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
