import re

import bs4

from . import preserve, keep, trash, VITAL, MAIN, EXTRA

def criteria(url: str):
    pattern = re.compile(r'((stackexchange|stackoverflow|stackapps|superuser|serverfault|askubuntu)\.com|mathoverflow.net)\/questions\/.*\/')
    return pattern.search(url)

def yoink(soup: bs4.BeautifulSoup):
    question = soup.find(class_='question')
    keep(question, MAIN, label='question')
    prose = question.find(class_='s-prose')
    preserve(prose, MAIN)
    trash(prose.aside, EXTRA)
    
    for com_list in soup(class_='comments-list'):
        keep(com_list, MAIN, 'comments')
        for comment in com_list(class_='comment'):
            keep(comment, MAIN)
            preserve(comment.find(class_='comment-score'), EXTRA)
            preserve(comment.find(class_='comment-copy'), MAIN)

    for votes in soup(class_='js-vote-count'):
        preserve(votes, EXTRA)
    
#    keep(soup.find(id='answers'))

    for i, answer in enumerate(soup(class_='answer')):
        keep(answer, MAIN if i else VITAL, label="answer")
        preserve(answer.find(class_='s-prose'), VITAL)

