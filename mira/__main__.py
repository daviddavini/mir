import subprocess
from argparse import ArgumentParser
from urllib.parse import urlencode

from .filter import filter
from .fetch import fetch

def search_url(query):
    query = " ".join(query)
    query = urlencode({'q': query})
    return f'www.duckduckgo.com/?{query}'

def main():
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-r', '--reload', default=False)
    subparsers = parser.add_subparsers(dest='command')
    parse_goto = subparsers.add_parser('goto', aliases='g')
    parse_goto.set_defaults(reload=True)
    parse_goto.add_argument('url')
    parse_search = subparsers.add_parser('search', aliases='s')
    parse_search.set_defaults(reload=True)
    parse_search.add_argument('query', nargs='+')
    args = parser.parse_args()

    if args.command == 'search':
        url = search_url(args.query)
    elif args.command == 'goto':
        url = args.url

    # use lynx to get the html
    html = fetch(url, args.reload)

    # filter the html, yoinking all the gunk
    new_html = filter(url, html, args.verbose)

    # send the result to w3m for display
    subprocess.run(['w3m', '-T', 'text/html', '-dump'], input=new_html.encode())

if __name__ == '__main__':
    main()
