from scraper import scraper

@scraper
class Wikipedia:
    paragraphs: list[str] = '.mw-content-ltr p:not(.mw-empty-elt)'
