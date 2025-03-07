from scraper import scraper

@scraper
class Comment:
    body: str = '.comment_body > .md'
    replies: list['Comment'] = '.replies .comment'

@scraper
class Reddit:
    title = '.post_title'
    body: str = '.post_body'
    comments: list[Comment] = '.comment'

