from urllib.parse import urlparse
import copy

from bs4 import BeautifulSoup
from bs4.element import Tag

from .yoinks import duckduckgo, stackexchange, cnn, bbc, github

def keepers(soup, level):
    if hasattr(soup, 'keep') and soup.keep and soup.level <= level:
        return [soup]
    if isinstance(soup, Tag):
        return sum([keepers(x, level) for x in soup.children], [])
    return []

def trashup(tag, level):
    todelete = []
    for x in tag.children:
        if hasattr(x, 'trash') and x.trash and x.level > level:
            todelete.append(x)
        if isinstance(x, Tag):
            trashup(x, level)
    for x in todelete:
        x.decompose()

def cleanup(soup, tag, level=1e100, depth=1):
    keeps = []
    for x in tag.children:
        keeps.extend(keepers(x, level))
    keeps = [x for x in keeps if x.text.strip()]
    tag.clear()
    for x in keeps:
        if x.keep == 'preserve':
            trashup(x, level)
        else:
            cleanup(soup, x, level, depth+1)
        if level > 0 and hasattr(x, 'label') and x.label:
            x.insert(0, soup.new_tag(f'h{min(depth,6)}', string=x.label.title()+':'))
        tag.append(copy.copy(x))

def filter(url: str, html: str, mode: int):
    if mode == 4:
        return html, False
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
        tag.decompose()
    for tag in soup(class_=['header', 'footer']):
        tag.decompose()

    for tag in soup(['aside', 'details', 'address']):
        tag.decompose()

    for tag in soup(role='navigation'):
        tag.decompose()
    for tag in soup(attrs={'aria-controls':'navigation'}):
        tag.decompose()

    # call the yoink method specific to the website
    yoink = True
    if stackexchange.criteria(url):
        stackexchange.yoink(soup)
    elif duckduckgo.criteria(url):
        duckduckgo.yoink(soup)
    elif cnn.criteria(url):
        cnn.yoink(soup)
    elif bbc.criteria(url):
        bbc.yoink(soup)
    elif github.criteria(url):
        github.yoink(soup)
    else:
        yoink = False

    if yoink:
        cleanup(soup, soup.body, mode)

    # label all of the links with numbers
    for i, link in enumerate(soup('a')):
        link.insert(0, f'[{i}] ')
    new_html = str(soup)
    return new_html, yoink

