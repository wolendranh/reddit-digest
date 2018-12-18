import argparse
import time

from markdown2 import Markdown
import praw

try:
    from settings import CREDENTIALS, SUBREDDIT, LINK_PATTERNS
except ImportError:
    raise Exception('please define variables in your settings file.')


def get_submissions(ups=None, subreddit=None):
    if not subreddit:
        raise Exception('please provide subreddit object')
    for submission in subreddit.submissions(start_timestamp, end_timestamp):
        if ups and submission.ups >= ups:
            yield submission


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("start")
    parser.add_argument("end")
    parser.add_argument("ups")

    args = parser.parse_args()
    start_date, end_date = time.strptime(args.start, '%Y-%m-%d'), time.strptime(args.end, '%Y-%m-%d')
    ups = int(args.ups)

    reddit = praw.Reddit(**CREDENTIALS)
    python_subreddit = reddit.subreddit(SUBREDDIT)

    start_timestamp = time.mktime(start_date)
    end_timestamp = time.mktime(end_date)

    markdown = Markdown(extras=["link-patterns"], link_patterns=LINK_PATTERNS)

    # write to markdown file with links embedded
    with open('links.md', 'w') as file:
        id = 1
        for submission in get_submissions(ups=ups, subreddit=python_subreddit):
            file.write(
                '  '.join(
                    [
                        str(id),
                        markdown.convert(submission.shortlink + '\n' + submission.title),
                    ]))
            id += 1
