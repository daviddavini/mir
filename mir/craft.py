from pathlib import Path
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from .constants import CURRENT_PATH
from .fetch import fetch_filtered

def search_url(query):
    query = " ".join(query)
    query = urlencode({'q': query})
    return f'www.duckduckgo.com/?{query}'

def hyperlinks(html):
    soup = BeautifulSoup(html, 'html.parser')
    return [l['href'] for l in soup('a')]

def normalize(url, link):
    if link.startswith('//'):
        return f'https:{link}'
    if link.startswith('/'):
        protocol, rest = url.split('://',1)
        domain, _ = rest.split('/',1)
        return protocol + '://' + domain + link
    return link

def follow_url(target):
    url = CURRENT_PATH.read_text().splitlines()[-1]
    html = fetch_filtered(url)
    links = hyperlinks(html)
    links = [normalize(url, l) for l in links]
    return links[int(target)]
