import urllib

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/91.0.4472.106 Safari/537.36",
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
}


def get_metacritic(game):
    platforms_to_metacritic = {
        "ps5": "PS5",
        "ps4": "PS4",
        "ps3": "PS3",
        "ps2": "PS2",
        "xbox series x": "XBSX",
        "xbox one": "XONE",
        "xbox 360": "X360",
        "xbox": "XBOX",
        "switch": "Switch",
        "pc": "PC",
    }
    game = game.lower()
    selected_platform = None
    for platform in platforms_to_metacritic.keys():
        if platform in game:
            selected_platform = platform
            game = game.replace(selected_platform, "").strip()
            selected_platform = platforms_to_metacritic[selected_platform]
    for i in range(2):
        url = f"https://www.metacritic.com/search/game/{game}/results?sort=relevancy&page={i}"
        text = requests.get(url, headers=headers).text
        soup = BeautifulSoup(text, "lxml")
        li_tags = soup.find_all("li", class_=["result first_result", "result"])
        for li_tag in li_tags:
            platform = li_tag.find("span", class_="platform")
            if not platform:
                continue
            platform = platform.text
            game_name = li_tag.find("a", href=True).text.strip()
            score = li_tag.find("span").text
            platform_and_date = li_tag.find("p").text
            platform_and_date = " ".join(platform_and_date.split())
            a_tag = li_tag.find("a", href=True)
            site = f"https://www.metacritic.com{a_tag['href']}"
            output_string = (
                f"Metacritic <{game_name} ({platform_and_date})>: {score} ~ {site}"
            )
            if not selected_platform:
                return output_string
            if selected_platform == platform:
                return output_string
    output_string = f"Metacritic <{game}>: no results."
    return output_string


def get_seriea():
    url = "https://www.tuttosport.com/live/classifica-serie-a"
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, "lxml")
    tr_tags = soup.find_all("tr")
    heading = tr_tags[0].get_text(separator=" ")
    output_string = f"{heading}\n"
    for i in range(1, len(tr_tags)):
        name_team = tr_tags[i].find("a", href=True).text
        output_string += f"{str(i)} {name_team} "
        statistics = tr_tags[i].find_all("td")[2:]
        for stat in statistics:
            stat = stat.text
            output_string += f"{stat} "
        output_string += "\n"
    return output_string


def get_f1():
    url = "https://sport.sky.it/formula-1/classifiche"
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, "lxml")
    tr_tags = soup.find_all("tr", class_="ftbl__top-drivers__body-row")
    string_bot = ""
    for tr_tag in tr_tags:
        player = tr_tag.find_all("span", class_="ftbl__top-drivers__body-cell-span")
        string_player = ""
        for attribute in player:
            string_player += f"{attribute.text} "
        string_bot += f"{string_player.strip()}\n"
    return string_bot


def get_f1team():
    url = "https://sport.sky.it/formula-1/classifiche"
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, "lxml")
    tr_tags = soup.find_all("tr", class_="ftbl__top-motorsports-teams__body-row")
    string_bot = ""
    for tr_tag in tr_tags:
        player = tr_tag.find_all(
            "span", class_="ftbl__top-motorsports-teams__body-cell-span"
        )
        string_player = ""
        for attribute in player:
            string_player += f"{attribute.text} "
        string_bot += f"{string_player.strip()} \n"
    return string_bot


def get_motogp():
    url = "https://sport.sky.it/motogp/classifiche"
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, "lxml")
    tr_tags = soup.find_all("tr", class_="ftbl__top-drivers__body-row")
    string_bot = ""
    for tr_tag in tr_tags:
        player = tr_tag.find_all("span", class_="ftbl__top-drivers__body-cell-span")
        string_player = ""
        for attribute in player:
            string_player += f"{attribute.text} "
        string_bot += f"{string_player.strip()}\n"
    return string_bot


def get_motogpteam():
    url = "https://sport.sky.it/motogp/classifiche"
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, "lxml")
    tr_tags = soup.find_all("tr", class_="ftbl__top-motorsports-teams__body-row")
    string_bot = ""
    for tr_tag in tr_tags:
        player = tr_tag.find_all(
            "span", class_="ftbl__top-motorsports-teams__body-cell-span"
        )
        string_player = ""
        for attribute in player:
            string_player += f"{attribute.text} "
        string_bot += f"{string_player.strip()}\n"
    return string_bot


def get_googlesearch(text):
    text = urllib.parse.quote_plus(text)
    url = (
        "https://google.com/search?q="
        + text
        + "&aqs=chrome.0.69i59j46j0l4j46i175i199j69i60.2048j0j4&sourceid=chrome&ie=UTF-8"
    )
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, "lxml")
    div_link = soup.find("div", class_="yuRUbf")
    link = "<" + div_link.a["href"] + ">"
    first_result_div = soup.find("div", class_="IsZvec")
    desciption_div = first_result_div.find(
        "div", class_="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc"
    )
    text = desciption_div.text
    text_bot = text + " - " + link
    return text_bot
