import re

import bs4

from . import preserve, keep, trash, ZEN, VITAL, MAIN, EXTRA

def criteria(url: str):
    pattern = re.compile(r'duckduckgo.com/.*\?q=.*')
    return pattern.search(url)

def yoink(soup: bs4.BeautifulSoup):
    table = soup.select('table:has(.result-link)')[0]
    keep(table)
    for tr in table.children:
        keep(tr)
    for i, link in enumerate(soup(class_='result-link')):
        preserve(link, VITAL if i>=2 else ZEN)
    for snippet in soup(class_='result-snippet'):
        preserve(snippet, EXTRA)
    for text in soup(class_='link-text'):
        preserve(text, MAIN)
