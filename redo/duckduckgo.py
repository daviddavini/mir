from scraper import scraper

@scraper
class Result:
    title: str = '.result__title'
    url: str = '.result__url'
    snippet: str = '.result__snippet'

@scraper
class DuckDuckGo:
    results: list[Result] = '.result'

