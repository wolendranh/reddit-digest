import argparse
import datetime

import praw
from psaw import PushshiftAPI

try:
    from settings import CREDENTIALS, SUBREDDIT
except ImportError:
    raise Exception('please define variables in your settings file.')


def get_submissions(api=None, ups=None, start=None, end=None, subreddit=None, limit=None):
    if not subreddit:
        raise Exception('please provide subreddit object')

    for sub in api.search_submissions(after=start,
                                      before=end,  
                                      subreddit=subreddit,
                                      limit=limit,
                                      filter=['url', 'author', 'title', 'subreddit']):
        if ups and sub.ups >= ups:
            yield sub


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("start")
    parser.add_argument("end")
    parser.add_argument("ups", type=int)
    parser.add_argument("--limit", required=False, default=None, type=int)

    args = parser.parse_args()
    start_date, end_date = datetime.datetime.strptime(args.start,  '%Y-%m-%d'), \
                           datetime.datetime.strptime(args.end, '%Y-%m-%d')
    ups = args.ups

    reddit = praw.Reddit(**CREDENTIALS)
    api = PushshiftAPI(reddit)

    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    with open('links.html', 'w') as file:
        _id = 1
        for submission in get_submissions(api=api, ups=ups, start=start_timestamp,
                                          end=end_timestamp, subreddit=SUBREDDIT, limit=args.limit):
            file.write("""
            <p>{id}&emsp;<a href='{url}' target='blank'>link&emsp;</a>{title}&emsp;<b>{ups}</b></p>
            """.format(
                id=_id,
                url=submission.shortlink,
                title=submission.title,
                ups=submission.ups
            ))
            _id += 1
