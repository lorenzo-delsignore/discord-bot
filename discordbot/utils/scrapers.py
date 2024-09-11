import aiohttp
from bs4 import BeautifulSoup


async def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/91.0.4472.106 Safari/537.36",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            return await resp.text()


async def get_multiplayerit():
    url = "https://multiplayer.it/articoli/notizie/"
    text = await get_html(url)
    soup = BeautifulSoup(text, "lxml")
    list_news = []
    div_news = soup.find_all("div", class_="media-body")
    for news in div_news:
        titles = news.find("a", class_="text-decoration-none stretched-link")
        if titles is None:
            continue
        title_news = titles.text.strip()
        link_news = f'https://multiplayer.it{titles["href"]}'
        list_news.append(("multiplayer.it", link_news, title_news))
    return list_news


async def get_everyeyeit():
    url = "https://www.everyeye.it/notizie/"
    text = await get_html(url)
    soup = BeautifulSoup(text, "lxml")
    list_news = []
    div_news = soup.find_all("div", class_="testi_notizia")
    for news in div_news:
        titles = news.find("a")
        title_news = titles["title"]
        link_news = titles["href"]
        list_news.append(("everyeye.it", link_news, title_news))
    return list_news


async def get_spaziogamesit():
    url = "https://www.spaziogames.it/videogiochi/news/"
    text = await get_html(url)
    soup = BeautifulSoup(text, "lxml")
    list_news = []
    div_news = soup.find_all("div", class_="post_template_standard_text")
    for news in div_news:
        titles = news.find("a")
        title_news = titles.text
        link_news = titles["href"]
        list_news.append(("spaziogames.it", link_news, title_news))
    return list_news


async def get_eurogamerit():
    url = "https://www.eurogamer.it/archive/news"
    text = await get_html(url)
    soup = BeautifulSoup(text, "lxml")
    list_news = []
    div_news = soup.find_all("div", class_="compact-archive-item")
    for news in div_news:
        titles = news.find("a")
        title_news = titles["title"]
        link_news = f'https://www.eurogamer.it{titles["href"]}'
        list_news.append(("eurogamer.it", link_news, title_news))
    return list_news


async def get_ignit():
    url = "https://it.ign.com/"
    text = await get_html(url)
    soup = BeautifulSoup(text, "lxml")
    list_news = []
    article_news = soup.find_all("article", class_="article NEWS")
    for news in article_news:
        titles = news.find("a")
        title_news = news.find("h3").text
        link_news = titles["href"]
        list_news.append(("it.ign.com", link_news, title_news))
    return list_news


async def get_pcgamercom():
    url = "https://www.pcgamer.com/uk/news/"
    text = await get_html(url)
    soup = BeautifulSoup(text, "lxml")
    list_news = []
    a_tag = soup.find_all("a", class_="article-link")
    for tag in a_tag:
        title_news = tag["aria-label"]
        link_news = tag["href"]
        list_news.append(("pcgamer.com", link_news, title_news))
    return list_news
