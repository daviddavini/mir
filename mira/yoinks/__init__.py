VITAL = 0
MAIN = 5
EXTRA = 10

def keep(soup, level=0, label=None):
    if not soup:
        return
    soup.keep = True
    soup.level = level
    soup.label = label

def preserve(soup, level=0, label=None):
    if not soup:
        return
    soup.keep = 'preserve'
    soup.level = level
    soup.label = label

def trash(soup, level=1e100):
    if not soup:
        return
    soup.trash = True
    soup.level = level

