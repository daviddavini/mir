import re

import bs4
from bs4.element import Tag

from . import preserve, keep, trash, ZEN, VITAL, MAIN, EXTRA

def criteria(url: str):
    pattern = re.compile(r'cnn.com\/\d+\/\d+\/\d+\/\S+\/\S+\/')
    return pattern.search(url)

def yoink(soup: bs4.BeautifulSoup):
    article = soup.find('article')
    keep(article)

    headline = soup.find(class_='headline')
    keep(headline, MAIN)
    preserve(headline.h1, MAIN)
    preserve(headline.find(class_='byline__names'), EXTRA)
    preserve(headline.find(class_='timestamp'), MAIN)

    #import pdb; pdb.set_trace()
    #for image in article(class_='inline-placeholder'):
    #    preserve(image, EXTRA, label='figure')
    for heading in article(class_='subheader'):
        preserve(heading)

    for i, p in enumerate(article(class_='paragraph')):
        preserve(p)

#    first_heading = False
#    for x in article.p.parent.children:
#        if isinstance(x, Tag) and (x.h2 or x.strong):
#            first_heading = True
#        if first_heading:
#            trash(x, VITAL)

