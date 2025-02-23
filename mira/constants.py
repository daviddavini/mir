from pathlib import Path

CACHE_DIR = Path.home() / '.mira' / 'raw'
CACHE_DIR.mkdir(parents=True, exist_ok=True)

CLEAN_DIR = Path.home() / '.mira' / 'clean'
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

CURRENT_PATH = Path.home() / '.mira' / 'current'
