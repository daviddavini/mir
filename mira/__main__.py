import subprocess
from argparse import ArgumentParser

from .craft import search_url, follow_url
from .fetch import fetch
from .filter import filter
from .constants import CURRENT_PATH
from .constants import CACHE_DIR, CLEAN_DIR
from .fetch import filename

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
    parse_follow = subparsers.add_parser('follow', aliases='f')
    parse_follow.set_defaults(reload=True)
    parse_follow.add_argument('target')
    args = parser.parse_args()

    if args.command in ['search', 's']:
        url = search_url(args.query)
    elif args.command in ['goto', 'g']:
        url = args.url
    elif args.command in ['follow', 'f']:
        url = follow_url(args.target)
    elif not args.command:
        url = CURRENT_PATH.read_text()

    CURRENT_PATH.write_text(url)

    # use lynx to get the html
    new_url, html = fetch(url, args.reload)

    # filter the html, yoinking all the gunk
    new_html = filter(new_url, html, args.verbose)

    # cache under the original url
    html_path = CLEAN_DIR / f'{filename(url)}.html'
    html_path.write_text(new_html)

    # send the result to w3m for display
    subprocess.run(['w3m', '-T', 'text/html', '-dump'], input=new_html.encode())

if __name__ == '__main__':
    main()
