import time

import aiohttp
import asyncio

async def checker(nickname, session):
    url = f'https://api.worldoftanks.eu/wot/account/list/?application_id=demo&search={nickname}'
    time.sleep(0.5)
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if data.get('data')[0]['nickname'] == nickname:
                print(f'Username {nickname} is available.')
            else:
                print(f'Username {nickname} is not available.')
        elif response.status == 409:  # Pokud je status kód 409, považuje se jméno také za dostupné
            print(f'Username {nickname} is available due to status code 409.')
        else:
            print(f'Failed to fetch data for {nickname}: Status code {response.status}')

async def main():
    # Načte soubor s přezdívkami
    with open('nickname.txt', 'r') as f:
        nicknames = f.read().strip().split('\n')

    # Vytvoří session pro asynchronní požadavky
    async with aiohttp.ClientSession() as session:
        tasks = [checker(nickname, session) for nickname in nicknames]
        await asyncio.gather(*tasks)

# Spustí asynchronní smyčku
asyncio.run(main())