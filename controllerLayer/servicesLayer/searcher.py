import json
import os

import aiohttp
from dotenv import load_dotenv

from .film_card_model import FilmCardModel

load_dotenv()

GOOGLE_API_URL = "https://www.googleapis.com/customsearch/v1"
KINOPOISK_API_URL = "https://api.kinopoisk.dev/v1.4"
KPOISK_URL = "https://flicksbar.mom/film"
JSON_API_TOKEN = os.environ['JSON_API_TOKEN']
CSE_TOKEN = os.environ["CSE_TOKEN"]
X_API_KEY = os.environ["KINOPOISK_TOKEN"]


class Searcher:
    """
    Class to search info and links to asked films
    """
    def __init__(self):
        self.session = None

    async def fetch(self, url: str,
                    params: dict[str, str],
                    headers: dict[str, str]) -> json:
        """
        Fetch asked url with need parameters and return json response.
        @param url: url to search
        @param params: https params
        @param headers: https headers
        @return json: https response
        """
        self.session = aiohttp.ClientSession()
        async with self.session as session:
            async with session.get(url,
                                   params=params,
                                   headers=headers) as response:
                content_type = response.headers.get("Content-Type", "")
                if not content_type.startswith("application/json"):
                    text = await response.text()
                    print(f'Response body: {text}')
                    raise Exception(f'Unexpected content type: {content_type}')

                data = await response.json()
                return data

    async def search_link(self, film_name: str) -> list[str]:
        """
        Search film by name in google cse and return list of links
        @param film_name: film name to search for
        @return: found
        """
        film_query: str = f"смотреть+{film_name}+кино+онлайн"

        url = GOOGLE_API_URL
        params = {
            'q': film_query,
            'key': JSON_API_TOKEN,
            'cx': CSE_TOKEN
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        data: json = await self.fetch(url, params, headers)
        links_list: list[str] = 4 * []
        for i in range(4):
            link_to_film = data['items'][i]['link']
            links_list.append(link_to_film)
        return links_list

    async def search_film_info(self, film_name: str) -> 'FilmCardModel':
        '''
        Send query to kinopoisk api to get film card
        @param film_name: film name to search for
        @return found FilmCardModel
        '''
        url = f"{KINOPOISK_API_URL}/movie/search"

        params = {
            "page": 1,
            "limit": 1,
            "query": film_name,
        }
        headers = {
            "accept": "application/json",
            "X-API-KEY": X_API_KEY
        }
        data: json = await self.fetch(url, params, headers)

        direct_url: str = f"{KPOISK_URL}/{data['docs'][0]['id']}"

        return FilmCardModel.from_json(data, direct_url)

    async def start(self):
        """Startup aoithhp session"""
        self.session = aiohttp.ClientSession()

    async def close(self):
        """Close aoithhp session"""
        await self.session.close()
