import re

import bs4

from . import preserve, keep, trash, VITAL, MAIN, EXTRA

def criteria(url: str):
    pattern = re.compile(r'google.com/search')
    return pattern.search(url)

def yoink(soup: bs4.BeautifulSoup):
    table = soup.select('table:has(.result-link)')[0]
    keep(table)
    for link in soup.select('tr:has(.result-link)'):
        preserve(link, VITAL)
    for snippet in soup.select('tr:has(.result-snippet)'):
        preserve(snippet, EXTRA)
    for text in soup.select('tr:has(.link-text)'):
        preserve(text, MAIN)
