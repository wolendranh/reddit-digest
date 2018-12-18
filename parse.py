import argparse
import datetime

from markdown2 import Markdown
import praw
from psaw import PushshiftAPI

try:
    from settings import CREDENTIALS, SUBREDDIT, LINK_PATTERNS
except ImportError:
    raise Exception('please define variables in your settings file.')


def get_submissions(api=None, ups=None, start=None, end=None, subreddit=None):
    if not subreddit:
        raise Exception('please provide subreddit object')

    for sub in api.search_submissions(after=start,
                                      subreddit=subreddit,
                                      filter=['url', 'author', 'title', 'subreddit'],
                                      limit=10):
        if ups and sub.ups >= ups:
            yield sub


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("start")
    parser.add_argument("end")
    parser.add_argument("ups")

    args = parser.parse_args()
    start_date, end_date = datetime.datetime.strptime(args.start,  '%Y-%m-%d'), \
                           datetime.datetime.strptime(args.end, '%Y-%m-%d')
    ups = int(args.ups)

    reddit = praw.Reddit(**CREDENTIALS)
    api = PushshiftAPI(reddit)

    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    markdown = Markdown(extras=["link-patterns"], link_patterns=LINK_PATTERNS)

    # write to markdown file with links embedded
    with open('links.md', 'w') as file:
        _id = 1
        for submission in get_submissions(api=api, ups=ups, start=start_timestamp,
                                          end=end_timestamp, subreddit=SUBREDDIT):
            print(submission.selftext)
            file.write(
                '  '.join(
                    [
                        str(_id),
                        markdown.convert(submission.shortlink + '\n' + submission.title),
                    ]))
            _id += 1
