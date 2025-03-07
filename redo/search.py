from urllib.parse import urlencode
import sys

from fetch import fetch

from stackoverflow import StackOverflow
from safereddit import SafeReddit
from duckduckgo import DuckDuckGo
from wikipedia import Wikipedia

def search(query):
    html = fetch('duckduckgo.com/html/search?'+urlencode({'q':query}))
    ddg = DuckDuckGo(html)
    return [res.url for res in ddg.results]

results = search(" ".join(sys.argv[1:]))
for res in results:
    if 'stackoverflow.com' in res:
        html = fetch(res)
        print(StackOverflow(html).answers[0].body)
        break
    if 'wikipedia.org' in res:
        html = fetch(res)
        print(Wikipedia(html).paragraphs[0])
        break
    if False and 'reddit.com' in res:
        res = res.replace('www.reddit.com','safereddit.com')
        html = fetch(res)
        print(SafeReddit(html).comments[0].body)
        break
