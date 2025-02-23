from pathlib import Path
import subprocess
from base64 import b64encode

CACHE_DIR = Path.home() / '.mira'
CACHE_DIR.mkdir(exist_ok=True)

def fetch(url, reload=False):
    enc = b64encode(url.encode()).decode()
    html_path = CACHE_DIR / f'{enc}.html'
    if html_path.exists():
        return html_path.read_text()
    html = subprocess.check_output(['lynx', '-source', url])
    html = html.decode()
    html_path.write_text(html)
    return html
