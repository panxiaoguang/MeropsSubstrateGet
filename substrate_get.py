import ssl
import argparse
import asyncio
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import aiohttp
parser = argparse.ArgumentParser(
    description='YOU CAN USE IT TO DOWNLOAD ALL SUBSTRATES OF ONE PROTEIN FAMILY')
parser.add_argument('--fm', '-f', help='please input your family number!')
parser.add_argument('--out', '-o', help='please input your outputdir!')
args = parser.parse_args()
protein_letters_1to3 = {
    'A': 'Ala', 'C': 'Cys', 'D': 'Asp',
    'E': 'Glu', 'F': 'Phe', 'G': 'Gly', 'H': 'His',
    'I': 'Ile', 'K': 'Lys', 'L': 'Leu', 'M': 'Met',
    'N': 'Asn', 'P': 'Pro', 'Q': 'Gln', 'R': 'Arg',
    'S': 'Ser', 'T': 'Thr', 'V': 'Val', 'W': 'Trp',
    'Y': 'Tyr',
}
table = []


def protein_letters_3to1(x):
    new_dct = dict((x[1], x[0]) for x in protein_letters_1to3.items())
    if x in new_dct:
        return new_dct[x]
    else:
        return " "


def get_urls(fm):
    url = "https://www.ebi.ac.uk/merops/cgi-bin/famsum?family={}".format(fm)
    result = requests.get(url).content
    root = "https://www.ebi.ac.uk"
    soup = BeautifulSoup(result, 'lxml')
    tab = soup.select('td[align="center"] > a')
    urls = {heihei.get_text(): root+heihei.get("href") for heihei in tab}
    return urls


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.read()


async def parse_substrate(html):
    sub_dct = {}
    soup = BeautifulSoup(html, 'lxml')
    tab = soup.select('tr')
    for tr in tab:
        if tr.select('td'):
            sub_dct["".join([protein_letters_3to1(haha.get_text()) for haha in tr.select(
                'td')[6:14]])] = tr.select('td')[0].get_text()
    return sub_dct
# async def parse_Enzyme(html):
#    soup = BeautifulSoup(html, 'lxml')
#    tab = soup.find("table", {'summary': 'Activity'})
#    if tab:
#        Catalytictype = tab.select("tr")[1].select("td")[1].get_text()
#        return Catalytictype


async def download_substrate(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        return await parse_substrate(html)
# async def download_Enzyme(url):
#    async with aiohttp.ClientSession() as session:
#        html = await fetch(session, url)
#        return await parse_Enzyme(html)


async def parse_Merops(sem, name, url):
    # cat = await download_Enzyme(url)
    async with sem:
        fina = await download_substrate(url.replace("pepsum", "substrates"))
        print("downloading database in url :{}".format(
        url.replace("pepsum", "substrates")))
        if fina:
            pachong = [(name, val, key) for key, val in fina.items()]
            table.extend(pachong)

sem = asyncio.Semaphore(50)
loop = asyncio.get_event_loop()
tasks = [parse_Merops(sem, name, url)
         for name, url in get_urls(args.fm).items()]
tasks = asyncio.wait(tasks)
loop.run_until_complete(tasks)
df = pd.DataFrame(
    table, columns=['merops_id', 'substrate', 'sequence'])
df.to_csv(os.path.join(args.out, "result.csv"), index=False)
print("All done! please check your result file.")
