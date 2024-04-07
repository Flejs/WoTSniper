import aiohttp
import asyncio
import time

async def checker(nickname, session):
    url = f'https://eu.wargaming.net/personal/account/nicknames/{nickname}/'
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if data.get('spa_id') is None:
                print(f'Username {nickname} is available.')
            else:
                print(f'Username {nickname} is not available.')
        else:
            print(f'Failed to fetch data for {nickname}: Status code {response.status}')
    await asyncio.sleep(1)  # Adds an asynchronous delay after each request.

async def main():
    # Loads the file with nicknames
    with open('nickname.txt', 'r') as f:
        nicknames = f.read().strip().split('\n')

    # Creates a session for asynchronous requests
    async with aiohttp.ClientSession() as session:
        tasks = [checker(nickname, session) for nickname in nicknames]
        await asyncio.gather(*tasks)

# Starts the asynchronous loop
asyncio.run(main())
