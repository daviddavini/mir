import subprocess
import re
from hashlib import sha512
from base64 import b64encode
from urllib.parse import quote

from bs4 import BeautifulSoup

from .constants import CLEAN_DIR, CACHE_DIR

def filename(url):
    return sha512(url.encode()).hexdigest()
    return quote(url, '')
    return b64encode(url.encode()).decode()

def fetch_filtered(url):
    html_path = CLEAN_DIR / f'{filename(url)}.html'
    if html_path.exists():
        return html_path.read_text()
    return None

def _fetch(url, reload):
    html_path = CACHE_DIR / f'{filename(url)}.html'
    if not reload and html_path.exists():
        html = html_path.read_text()
    else:
        html = subprocess.check_output(['lynx', '-base', '-source', '-preparsed', url]).decode()
        html_path.write_text(html)
    return html

def fetch(url, reload=False):
    html = _fetch(url, reload)
    soup = BeautifulSoup(html, 'html.parser')
    meta_tag = soup.find('meta', attrs={'http-equiv': 'refresh'})
    if meta_tag:
        match = re.search(r'URL=([^\s]+)', meta_tag['content'])
        url = match.group(1)
        html = _fetch(url, reload)
    return url, html
