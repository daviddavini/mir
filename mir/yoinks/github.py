import re

import bs4

from . import preserve, keep, trash, ZEN, VITAL, MAIN, EXTRA

def criteria(url: str):
    return re.search(r'github.com/[^/]+/[^/]+', url)

def yoink(soup: bs4.BeautifulSoup):
    article = soup.article
    preserve(article, VITAL)

    seen_p = False
    for x in article.children:
        if x.name and (x.name == 'h2' or x.h2):
            if seen_p:
                break
        preserve(x, ZEN)
        if x.name and (x.name == 'p' or x.p):
            seen_p = True
