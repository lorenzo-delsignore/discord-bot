import datetime
import json
from configparser import ConfigParser

import aiohttp
from bs4 import BeautifulSoup

from discordbot.utils.scrapers import (
    get_eurogamerit,
    get_everyeyeit,
    get_ignit,
    get_multiplayerit,
    get_pcgamercom,
)


async def bot_send_news(client, list_news, dict_news, id_channel):
    for site, link_news, title_news in list_news:
        if site not in dict_news:
            dict_news[site] = {}
        dictvalues_news = dict_news.get(site)
        if link_news not in dictvalues_news:
            date_news = datetime.date.today().strftime("%Y-%m-%d")
            dict_news[site][link_news] = (title_news, date_news)
            channel = client.get_channel(id_channel)
            await channel.send(f"{title_news} {link_news}")


async def get_gamesnews(client):
    config = ConfigParser()
    config.read("config.ini")
    sites = {
        "it": {
            "https://multiplayer.it/articoli/notizie/": get_multiplayerit,
            "https://www.everyeye.it/notizie/": get_everyeyeit,
            #'https://www.spaziogames.it/videogiochi/news/': get_spaziogamesit,
            "https://www.eurogamer.it/archive/news": get_eurogamerit,
            "https://it.ign.com/": get_ignit,
        },
        "en": {
            "https://www.pcgamer.com/uk/news/": get_pcgamercom,
        },
    }
    dict_channels = {
        "gamenews_it": config["channels"].getint("id_gamenewsit"),
        "gamenews_en": config["channels"].getint("id_gamenewsen"),
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/91.0.4472.106 Safari/537.36",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    for language, sites in sites.items():
        for site, function in sites.items():
            async with aiohttp.ClientSession(headers=headers) as ses:
                async with ses.get(site) as response:
                    if response.status == 200:
                        text = await response.text()
                        soup = BeautifulSoup(text, "lxml")
                        with open("dictionary_news.json", "r") as f:
                            dict_news = json.load(f)
                        list_news = await function(soup)
                        id_channel = (
                            dict_channels["gamenews_it"]
                            if language == "it"
                            else dict_channels["gamenews_en"]
                        )
                        await bot_send_news(client, list_news, dict_news, id_channel)
                        with open("dictionary_news.json", "w") as f:
                            json.dump(dict_news, f)
