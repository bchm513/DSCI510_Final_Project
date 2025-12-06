
##### This is the file where I use PFF's API to get my transfer data from 2019-2024

import os
import json
import shutil
import asyncio
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential
import pandas as pd
import time 
from dotenv import load_dotenv
load_dotenv()

# print("API Key from env:", os.environ.get("PFF_API"))

@retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=1, min=1, max=10))
async def get_jwt_token(auth_url='https://api.profootballfocus.com/auth/login'):
    async with aiohttp.ClientSession() as session:
        data = {
            'x-api-key':os.environ['PFF_API']
        }
        async with session.post(auth_url, headers=data) as resp:
            resp.raise_for_status()
            result = await resp.json()
            return result["jwt"]

@retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=1, min=1, max=10))
async def fetch(session, url, token_ref):

    headers = {'Authorization': f'Bearer {token_ref["token"]}'}
    async with session.get(url, timeout=10, headers=headers) as resp:
        if resp.status == 401:
            token_ref['token'] = await get_jwt_token()
        else:
            resp.raise_for_status()
        return await resp.json()
    
async def fetch_all(key, urls, max_concurrency=20):
    token = await get_jwt_token()
    token_ref = {'token':token}
    results = []
    semaphore = asyncio.Semaphore(max_concurrency)  # throttle requests
    async with aiohttp.ClientSession() as session:
        async def bound_fetch(url):
            async with semaphore:
                return await fetch(session, url, token_ref)

        tasks = [asyncio.create_task(bound_fetch(url)) for url in urls]
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
    print(f"Finished {key}")
    return results

async def get_api_main(BASE_URL):
    seasons = [2019, 2020, 2021, 2022, 2023, 2024]
    urls = [BASE_URL.format(season=season) for season in seasons]

    results = await fetch_all("season_grades", urls)

    os.makedirs("../data", exist_ok=True)
    with open("../data/season_grades.json", "w") as f:
        json.dump(results, f, indent=2)


def join_ids_with_api(succeeded_ids_df, file_id):
    # import json
    
    ##### this was the original way I joined the data after retrieving it from the API
    ##### it takes a very long time so I am commenting it out, and for simplicity's sake I am only going to pull it from my google drive as I have been for other data
    ##### UNCOMMENT SECTION BELOW FOR ACTUAL JOINING

    # with open("../data/season_grades.json", "r") as fin:
    #     data = json.load(fin)

    # with open("../data/season_grades_filtered.json", "a") as f:
    #     f.write("[\n")
    #     for obj in data:
    #         # Loop through each player in the season
    #         for player in obj["season_grade"]:      
    #             for i, v in succeeded_ids_df.iterrows():
    #                 iter_pff_player_id = v["pff_player_id"]
    #                 iter_prev_season = v["prev_season"]

    #                 if player["player_id"] == iter_pff_player_id and player["season"] == iter_prev_season:
    #                     json.dump(player, f, indent=2)
    #                     f.write(",")
    #                     print(player)
                            
    #           # print(player)

    ##### this is the simplified version where I just pull the already joined data from my google drive
    ##### COMMENT THIS SECTION OUT FOR ACTUAL JOINING

    import requests
    import json
    import os

    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # Create directory if needed
    os.makedirs("../data", exist_ok=True)

    # Download the file
    response = requests.get(url)

    # Save to file
    with open("../data/season_grades_filtered.json", "wb") as f:
        f.write(response.content)

    # Or load directly as JSON
    data = json.loads(response.content)
    print(data)
            
            
