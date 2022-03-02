import asyncio
import datetime
import json
import urllib

from configparser import ConfigParser

import aiohttp
import discord
import requests

from bs4 import BeautifulSoup
from discord.ext import commands, tasks


config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
announcements = config['channels']['id_announcements']
intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=']', intents=intents)
token = config['bot']['token']
gamenews_it = config['channels'].getint('id_gamenewsit')
gamenews_en = config['channels'].getint('id_gamenewsen')
test_bot = config['channels'].getint('id_testbot')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/91.0.4472.106 Safari/537.36',
           'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7'}


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Superleague'))
    print(f'We have logged in as {client.user}')
    get_gamesnews.start()
    await asyncio.sleep(50)
    delete_news.start()


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    if message.content.startswith('hello'):
        await message.channel.send('Hello!')
    if message.content.startswith(']gamenews'):
        await message.channel.send(await get_gamesnews())
    await client.process_commands(message)


@client.event
async def on_member_update(before, after):
    pass


@client.event
async def on_member_join(member):
    channel = client.get_channel(announcements)
    await channel.send(f'Welcome to KlindaTV server {member.mention}. Enjoy your stay!')


@tasks.loop(minutes=30)
async def get_gamesnews():
    sites = {'https://multiplayer.it/articoli/notizie/': get_multiplayerit,
             'https://www.everyeye.it/notizie/': get_everyeyeit,
             'https://www.spaziogames.it/videogiochi/news/': get_spaziogamesit,
             'https://www.eurogamer.it/archive/news': get_eurogamerit,
             'https://it.ign.com/': get_ignit,
             'https://www.pcgamer.com/uk/news/': get_pcgamercom}
    for site, function in sites.items():
        async with aiohttp.ClientSession(headers=headers) as ses:
            async with ses.get(site) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = BeautifulSoup(text, 'lxml')
                    with open('dictionary_news.json', 'r') as f:
                        dict_news = json.load(f)
                    await function(soup, dict_news)
                    with open('dictionary_news.json', 'w') as f:
                        json.dump(dict_news, f)


async def get_multiplayerit(soup, dict_news):
    div_news = soup.find_all('div', class_='media-body')
    for news in div_news:
        titles = news.find('a', class_='text-decoration-none')
        title_news = titles.text.strip()
        link_news = f'https://multiplayer.it{titles["href"]}'

        await send_news('multiplayer.it', link_news, title_news, dict_news)


async def get_everyeyeit(soup, dict_news):
    div_news = soup.find_all('div', class_='testi_notizia')
    for news in div_news:
        titles = news.find('a')
        title_news = titles['title']
        link_news = titles['href']
        await send_news('everyeye.it', link_news, title_news, dict_news)


async def get_spaziogamesit(soup, dict_news):
    div_news = soup.find_all('div', class_='post_template_standard_text')
    for news in div_news:
        titles = news.find('a')
        title_news = titles.text
        link_news = titles['href']
        await send_news('spaziogames.it', link_news, title_news, dict_news)


async def get_eurogamerit(soup, dict_news):
    div_news = soup.find_all('div', class_='compact-archive-item')
    for news in div_news:
        titles = news.find('a')
        title_news = titles['title']
        link_news = f'https://www.eurogamer.it{titles["href"]}'
        await send_news('eurogamer.it', link_news, title_news, dict_news)


async def get_ignit(soup, dict_news):
    article_news = soup.find_all('article', class_='article NEWS')
    for news in article_news:
        div_news = soup.find('div', class_='m')
        titles = news.find('a')
        title_news = news.find('h3').text
        link_news = titles['href']
        await send_news('it.ign.com', link_news, title_news, dict_news)


async def get_pcgamercom(soup, dict_news):
    a_tag = soup.find_all('a', class_='article-link')
    for tag in a_tag:
        title_news = tag['aria-label']
        link_news = tag['href']
        await send_news('pcgamer.com', link_news, title_news, dict_news)


async def send_news(site, link_news, title_news, dict_news):
    dictvalues_news = dict_news.get(site)
    if link_news not in dictvalues_news:
        date_news = datetime.date.today().strftime('%Y-%m-%d')
        dict_news[site][link_news] = (title_news, date_news)
        if site[-2:] == 'it':
            channel = client.get_channel(gamenews_it)
        else:
            channel = client.get_channel(gamenews_en)
        await channel.send(f'{title_news} {link_news}')


@tasks.loop(hours=24)
async def delete_news():
    with open('dictionary_news.json', 'r') as f:
        dict_newsa = json.load(f)
    for site, dict in list(dict_newsa.items()):
        for site_news, news in list(dict.items()):
            date = news[1]
            date_news = datetime.datetime.strptime(date, '%Y-%m-%d')
            current_date = datetime.date.today()
            date_difference = current_date - date_news.date()
            if date_difference.days == 10:
                del dict[site_news]
                with open('dictionary_news.json', 'w') as f:
                    json.dump(dict_newsa, f)


@client.command()
@commands.has_role('Mod')
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')


@client.command()
@commands.has_role('Mod')
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


@client.command()
@commands.has_role('Mod')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')


@client.command()
async def google(ctx, *, question):
    text = get_googlesearch(question)
    await ctx.send(text)


def get_googlesearch(text):
    text = urllib.parse.quote_plus(text)
    url = 'https://google.com/search?q=' + text + \
        '&aqs=chrome.0.69i59j46j0l4j46i175i199j69i60.2048j0j4&sourceid=chrome&ie=UTF-8'
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    div_link = soup.find('div', class_='yuRUbf')
    link = '<' + div_link.a['href'] + '>'
    first_result_div = soup.find('div', class_='IsZvec')
    desciption_div = first_result_div.find(
        'div', class_='VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc')
    text = desciption_div.text
    text_bot = text + ' - ' + link
    return text_bot


@client.command()
async def seriea(ctx):
    text = seriea()
    await ctx.send(text)


def seriea():
    url = 'https://www.legaseriea.it/it/serie-a/classifica'
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, 'lxml')
    tr_tags = soup.find_all('tr', class_='')
    string = 'P TEAM PT \n'
    for tr_tag in tr_tags:
        pos = tr_tag.find('span', class_='pos').text
        team_name = tr_tag.find('img')['title']
        points = tr_tag.find('td', class_='blue').text
        string += f'{pos} {team_name} {points}\n'
        if pos == '20':
            break
    return string


@client.command()
async def f1(ctx):
    text = f1()
    await ctx.send(text)


def f1():
    url = 'https://sport.sky.it/formula-1/classifiche'
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, 'lxml')
    tr_tags = soup.find_all('tr', class_='ftbl__top-drivers__body-row')
    string_bot = ''
    for tr_tag in tr_tags:
        player = tr_tag.find_all(
            'span', class_='ftbl__top-drivers__body-cell-span')
        string_player = ''
        for attribute in player:
            string_player += f'{attribute.text} '
        string_bot += f'{string_player.strip()}\n'
    return string_bot


@client.command()
async def f1team(ctx):
    text = f1team()
    await ctx.send(text)


def f1team():
    url = 'https://sport.sky.it/formula-1/classifiche'
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, 'lxml')
    tr_tags = soup.find_all(
        'tr', class_='ftbl__top-motorsports-teams__body-row')
    string_bot = ''
    for tr_tag in tr_tags:
        player = tr_tag.find_all(
            'span', class_='ftbl__top-motorsports-teams__body-cell-span')
        string_player = ''
        for attribute in player:
            string_player += f'{attribute.text} '
        string_bot += f'{string_player.strip()} \n'
    return string_bot


@client.command()
async def motogp(ctx):
    text = motogp()
    await ctx.send(text)


def motogp():
    url = 'https://sport.sky.it/motogp/classifiche'
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, 'lxml')
    tr_tags = soup.find_all('tr', class_='ftbl__top-drivers__body-row')
    string_bot = ''
    for tr_tag in tr_tags:
        player = tr_tag.find_all(
            'span', class_='ftbl__top-drivers__body-cell-span')
        string_player = ''
        for attribute in player:
            string_player += f'{attribute.text} '
        string_bot += f'{string_player.strip()}\n'
    return string_bot


@client.command()
async def motogpteam(ctx):
    text = motogpteam()
    await ctx.send(text)


def motogpteam():
    url = 'https://sport.sky.it/motogp/classifiche'
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, 'lxml')
    tr_tags = soup.find_all(
        'tr', class_='ftbl__top-motorsports-teams__body-row')
    string_bot = ''
    for tr_tag in tr_tags:
        player = tr_tag.find_all(
            'span', class_='ftbl__top-motorsports-teams__body-cell-span')
        string_player = ''
        for attribute in player:
            string_player += f'{attribute.text} '
        string_bot += f'{string_player.strip()}\n'
    return string_bot


client.run(token)
