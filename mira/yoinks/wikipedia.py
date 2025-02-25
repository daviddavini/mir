import re

import bs4

from . import preserve, keep, trash, ZEN, VITAL, MAIN, EXTRA

def criteria(url: str):
    return re.search(r'wikipedia.org/wiki/[^/:]+$', url)

BIB = '#Notes,#References,#Footnotes,#Works_cited,#Further_reading,#External_links'
NOTES = f'#Works,#Publications,#Discography,#Filmography,#See_also,{BIB}'

def yoink(soup: bs4.BeautifulSoup):
    content = soup.select('.mw-content-ltr')[0]
    preserve(content, ZEN)

    #soup.select('(//*[contains(@class, 'mw-heading')]//h2)[1]/preceding::p')
    for x in content.select('[style="display:none"]'):
        trash(x)
    for x in content.select('[role="note"]'):
        trash(x, MAIN)
    #import pdb; pdb.set_trace()
    for x in soup.select('.ambox'):
        trash(x, EXTRA)
    for x in content.select('.mw-heading ~ *,.mw-heading'):
        trash(x, VITAL)
    for x in content.select(f'.mw-heading:has({NOTES}) ~ *'):
        trash(x, MAIN)
    for x in content.select(f'.mw-heading:has(> {NOTES})'):
        trash(x, MAIN)
    for x in content.select(f'.mw-heading:has(#Gallery)'):
        trash(x)
    for x in content.select(f'.gallery'):
        trash(x)
    for x in content.select(f'img'):
        trash(x)
    for x in content.select('.side-box'):
        trash(x, EXTRA)
    for x in content.select('.mw-collapsible,.mw-collapsed'):
        trash(x, EXTRA)
    for x in content.select('.infobox'):
        trash(x, MAIN)
    for x in content.select('.mw-editsection,figure'):
        trash(x)
    return
    before_h2 = True
    for x in main.children:
        if x.name and (x.name == 'h2' or x.h2):
            before_h2 = False
        preserve(x, ZEN if before_h2 else VITAL if before_suffix else MAIN)

