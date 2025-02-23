from urllib.parse import urlparse
import copy

from bs4 import BeautifulSoup
from bs4.element import Tag

from .yoinks import VITAL, MAIN, EXTRA
from .yoinks import duckduckgo, stackexchange

def keepers(soup, level):
    if hasattr(soup, 'keep') and soup.keep and soup.level <= level:
        return [soup]
    if isinstance(soup, Tag):
        return sum([keepers(x, level) for x in soup.children], [])
    return []

def trashup(tag, level):
    for x in tag.children:
        if hasattr(x, 'trash') and x.trash and x.level > level:
            x.decompose()
        if isinstance(x, Tag):
            trashup(x, level)

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
        if hasattr(x, 'label') and x.label:
            x.insert(0, soup.new_tag(f'h{min(depth,6)}', string=x.label.title()+':'))
        tag.append(copy.copy(x))

def filter(url: str, html: str, verbose: int):
    mode = {0:VITAL,1:MAIN,2:EXTRA}[verbose]
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style', 'nav', 'footer']):
        tag.decompose()

    # call the yoink method specific to the website
    yoink = True
    if stackexchange.criteria(url):
        stackexchange.yoink(soup)
    elif duckduckgo.criteria(url):
        duckduckgo.yoink(soup)
    else:
        yoink = False

    if yoink:
        cleanup(soup, soup.body, mode)
    new_html = str(soup)
    
    return new_html

