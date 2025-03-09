import subprocess

from typing import get_type_hints, get_origin, get_args
from bs4 import BeautifulSoup

def select_top(soup, sel):
    tags = []
    while True:
        tag = soup.select_one(sel)
        if not tag:
            break
        tags.append(tag.extract())
    return tags

def _scrape(soup, tp, sel):
    if get_origin(tp) == list:
        tp = get_args(tp)[0]
        return [_scrape(t, tp, None) for t in select_top(soup,sel)]
    else:
        s = soup.select_one(sel) if sel else soup
        if s is None:
            raise ValueError(f"Selector did not match any HTML element: {sel}")
        if tp == str:
            return s.get_text(' ', strip=True)
            return subprocess.run(['w3m','-T','text/html'],capture_output=True,text=True,input=str(s)).stdout.strip('\n')
        elif tp._is_scraper:
            return tp(s)

def scraper(cls):
    cls._is_scraper = True
    def __init__(self, html):
        soup = BeautifulSoup(html, 'html.parser') if type(html)==str else html
        members = [a for a in dir(self) if not (a.startswith('__') or callable(getattr(self,a)))]
        for attr in members:
            if attr == '_is_scraper':
                continue
            sel = getattr(self,attr)
            tp = get_type_hints(self.__class__).get(attr,str)
            val = _scrape(soup, tp, sel)
            setattr(self, attr, val)
    cls.__init__ = __init__
    return cls
