from scraper import scraper

@scraper
class Post:
    body = '.s-prose'
    comments: list[str] = '.comment-copy'

@scraper
class StackOverflow:
    header = '#question-header'
    question: Post = '.question'
    answers: list[Post] = '.answer'
