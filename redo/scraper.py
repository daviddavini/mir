from typing import get_type_hints, get_origin, get_args
from bs4 import BeautifulSoup

def _scrape(soup, tp, sel):
    if get_origin(tp) == list:
        tp = get_args(tp)[0]
        return [_scrape(t, tp, None) for t in soup.select(sel)]
    else:
        soup = soup.select_one(sel) if sel else soup
        if tp == str:
            return soup.get_text(strip=True)
        elif tp._is_scraper:
            return tp(soup)

def scraper(cls):
    cls._is_scraper = True
    def __init__(self, html):
        soup = BeautifulSoup(html, 'html.parser') if type(html)==str else html
        members = [a for a in dir(self) if not (a.startswith('__') or callable(getattr(self,a)))]
        for attr in members:
            if attr == '_is_scraper':
                continue
            sel = getattr(self,attr)
            tp = get_type_hints(self).get(attr,str)
            val = _scrape(soup, tp, sel)
            setattr(self, attr, val)
    cls.__init__ = __init__
    return cls
