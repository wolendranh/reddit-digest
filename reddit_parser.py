import heapq
import os
import re
import urllib.request

import nltk
from bs4 import BeautifulSoup as Soup
import praw
from psaw import PushshiftAPI

from settings import CREDENTIALS, SUBREDDIT


class RedditParser:
    reddit = None
    api = None
    parsed_submissions = []

    def __init__(self,):
        self.reddit = praw.Reddit(**CREDENTIALS)
        self.api = PushshiftAPI(self.reddit)

    def parse(self, ups=None, start=None, end=None, subreddit=SUBREDDIT, limit=None):
        for idx, sub in enumerate(self.get_submissions(ups, start, end, subreddit, limit)):
            self.store_to_file(submission=sub, identifier=idx)

    def get_submissions(self, ups=None, start=None, end=None, subreddit=None, limit=None):
        if not subreddit:
            raise Exception('please provide subreddit object')

        for sub in self.api.search_submissions(after=start,
                                               before=end,
                                               subreddit=subreddit,
                                               limit=limit,
                                               filter=['url', 'author', 'title', 'subreddit']):
            if ups and sub.ups >= ups:
                yield sub

    def get_highlight_color(self, ups):
        color = ''
        if 100 <= ups < 300:
            color = 'green'
        elif 300 <= ups < 500:
            color = 'orange'
        elif ups >= 500:
            color = 'red'
        return color

    def store_to_file(self, submission, identifier, file_name='links.html',):
        if identifier == 0:
            try:
                os.remove(file_name)
            except OSError:
                pass

        if submission.id not in self.parsed_submissions:
            with open(file_name, 'a') as file:
                file.write("""
                <p>{id}&emsp;<a href='{url}' target='blank'>link</a>&emsp;{title}&emsp;<b style="color:{color}">{ups}</b></p>
                """.format(
                    id=identifier,
                    url=submission.shortlink,
                    title=submission.title,
                    ups=submission.ups,
                    color=self.get_highlight_color(ups=submission.ups)

                ))
            self.parsed_submissions.append(submission.id)
