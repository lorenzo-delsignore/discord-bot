async def get_multiplayerit(soup):
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


async def get_everyeyeit(soup):
    list_news = []
    div_news = soup.find_all("div", class_="testi_notizia")
    for news in div_news:
        titles = news.find("a")
        title_news = titles["title"]
        link_news = titles["href"]
        list_news.append(("everyeye.it", link_news, title_news))
    return list_news


async def get_spaziogamesit(soup):
    list_news = []
    div_news = soup.find_all("div", class_="post_template_standard_text")
    for news in div_news:
        titles = news.find("a")
        title_news = titles.text
        link_news = titles["href"]
        list_news.append(("spaziogames.it", link_news, title_news))
    return list_news


async def get_eurogamerit(soup):
    list_news = []
    div_news = soup.find_all("div", class_="compact-archive-item")
    for news in div_news:
        titles = news.find("a")
        title_news = titles["title"]
        link_news = f'https://www.eurogamer.it{titles["href"]}'
        list_news.append(("eurogamer.it", link_news, title_news))
    return list_news


async def get_ignit(soup):
    list_news = []
    article_news = soup.find_all("article", class_="article NEWS")
    for news in article_news:
        titles = news.find("a")
        title_news = news.find("h3").text
        link_news = titles["href"]
        list_news.append(("it.ign.com", link_news, title_news))
    return list_news


async def get_pcgamercom(soup):
    list_news = []
    a_tag = soup.find_all("a", class_="article-link")
    for tag in a_tag:
        title_news = tag["aria-label"]
        link_news = tag["href"]
        list_news.append(("pcgamer.com", link_news, title_news))
    return list_news
