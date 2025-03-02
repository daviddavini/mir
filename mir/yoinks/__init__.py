ZEN = 0
VITAL = 1
MAIN = 2
EXTRA = 3

def keep(soup, level=0, label=None):
    if not soup or not soup.name:
        return
    soup.keep = True
    soup.level = min(soup.level or 1e100, level)
    soup.label = label

def preserve(soup, level=0, label=None):
    if not soup or not soup.name:
        return
    soup.keep = 'preserve'
    soup.level = min(soup.level or 1e100, level)
    soup.label = label

def trash(soup, level=1e100):
    if not soup or not soup.name:
        return
    soup.trash = True
    soup.level = max(soup.level or 0, level)
