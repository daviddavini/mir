import subprocess
from argparse import ArgumentParser

from .filter import filter

def main():
    parser = ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-m', '--mode', default='vital')
    args = parser.parse_args()
    url = args.url
    mode = args.mode

    # use lynx to get the html
    html = subprocess.check_output(['lynx', '-source', url])

    # filter the html, yoinking all the gunk
    new_html = filter(url, html, mode)

    # send the result to w3m for display
    subprocess.run(['w3m', '-T', 'text/html'], input=new_html.encode())

if __name__ == '__main__':
    main()
