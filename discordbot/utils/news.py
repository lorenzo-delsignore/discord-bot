import datetime
import json
from configparser import ConfigParser

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


async def get_gamenews(client):
    config = ConfigParser()
    config.read("config.ini")
    sites = {
        "it": [
            get_multiplayerit,
            get_everyeyeit,
            # get_spaziogamesit,
            get_eurogamerit,
            get_ignit,
        ],
        "en": [get_pcgamercom],
    }
    dict_channels = {
        "gamenews_it": config["channels"].getint("id_gamenewsit"),
        "gamenews_en": config["channels"].getint("id_gamenewsen"),
    }
    for language, sites in sites.items():
        for function in sites:
            with open("dictionary_news.json", "r") as f:
                dict_news = json.load(f)
            list_news = await function()
            id_channel = (
                dict_channels["gamenews_it"]
                if language == "it"
                else dict_channels["gamenews_en"]
            )
            await bot_send_news(client, list_news, dict_news, id_channel)
            with open("dictionary_news.json", "w") as f:
                json.dump(dict_news, f)
