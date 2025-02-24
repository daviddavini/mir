import re

import bs4

from . import preserve, keep, trash, ZEN, VITAL, MAIN, EXTRA

def criteria(url: str):
    pattern = re.compile(r'www.bbc.com/news/\S+')
    return pattern.search(url)

def yoink(soup: bs4.BeautifulSoup):
    article = soup.article
    preserve(article, ZEN)

    trash(article.h1, MAIN)
    trash(article.time, MAIN)

    first_heading = False
    for x in article.children:
        if x.h2:
            first_heading = True
        if first_heading:
            trash(x, VITAL)

    #for ul in article('ul'):
    #    trash(ul)
    for list in article(attrs={"data-component":"unordered-list-block"}):
        trash(list)

    for image in article(['figure', 'figcaption']):
        trash(image)
    for links in article(attrs={"data-component":"links-block"}):
        trash(links)
