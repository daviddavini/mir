import subprocess
import re
import os
from hashlib import sha512
from base64 import b64encode
from urllib.parse import quote
from pathlib import Path

from platformdirs import user_cache_dir
from bs4 import BeautifulSoup

CACHE_DIR = Path(user_cache_dir('mir','daviddavini')) / 'fetch'
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def _fetch(url):
    cache_filename = sha512(url.encode()).hexdigest()
    html_path = CACHE_DIR / f'{cache_filename}.html'
    if html_path.exists():
        html = html_path.read_text()
    else:
        html = subprocess.check_output(['lynx', '-base', '-source', url]).decode()
        html_path.write_text(html)
    return html

def redirect_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    meta_tag = soup.find('meta', attrs={'http-equiv': 'refresh'})
    if not meta_tag:
        return None
    match = re.search(r'URL=([^\s]+)', meta_tag['content'])
    url = match.group(1)
    return url

def fetch(url):
    new_url = url
    while new_url:
        url = new_url
        html = _fetch(url)
        new_url = redirect_url(html)
    return html
