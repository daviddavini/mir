import subprocess
import os
from argparse import ArgumentParser

from .craft import search_url, follow_url
from .fetch import fetch
from .filter import filter
from .constants import CURRENT_PATH
from .constants import CACHE_DIR, CLEAN_DIR
from .fetch import filename

def main():
    parent_parser = ArgumentParser(add_help=False)
    parent_parser.add_argument('-v', '--verbose', action='count', default=0)
    parent_parser.add_argument('-r', '--reload', action='store_true', default=False)
    parent_parser.add_argument('--raw', action='store_true', default=False)
    parser = ArgumentParser(parents=[parent_parser])
    subparsers = parser.add_subparsers(dest='command')
    parse_goto = subparsers.add_parser('goto', aliases='g', parents=[parent_parser])
    parse_goto.add_argument('url')
    parse_search = subparsers.add_parser('search', aliases='s', parents=[parent_parser])
    parse_search.add_argument('query', nargs='+')
    parse_follow = subparsers.add_parser('follow', aliases='f', parents=[parent_parser])
    parse_follow.add_argument('target', nargs='?', default=0)
    args = parser.parse_args()

    if args.command in ['search', 's']:
        url = search_url(args.query)
        CURRENT_PATH.write_text(url)
    elif args.command in ['goto', 'g']:
        url = args.url
        CURRENT_PATH.write_text(url)
    elif args.command in ['follow', 'f']:
        url = follow_url(args.target)
    elif not args.command:
        url = CURRENT_PATH.read_text()

    # use lynx to get the html
    new_url, html = fetch(url, args.reload)

    # filter the html, yoinking all the gunk
    new_html, yoink = filter(new_url, html, args.verbose)

    # cache under the original url
    html_path = CLEAN_DIR / f'{filename(url)}.html'
    html_path.write_text(new_html)

    # send the result to w3m for display
    if args.raw:
        print(new_html); return
    if not yoink:
        subprocess.run(['w3m', '-T', 'text/html'], input=new_html.encode())
        return
    size = os.get_terminal_size()
    output = subprocess.check_output(['w3m', '-T', 'text/html', '-dump', '-cols', str(size.columns)], input=new_html.encode()).decode()
    output = output.strip()
    if len(output.splitlines()) <= size.lines-2:
        print(output)
    else:
        subprocess.run(['less'], input=output.encode())

if __name__ == '__main__':
    main()
