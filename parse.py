import re
from datetime import datetime, date
import calendar
from pprint import pprint

from markdown2 import Markdown
import praw

try:
    from settings import CREDENTIALS, SUBREDDIT
except ImportError:
    raise Exception('please define variables in your settings file.')


def get_submissions(score=None, ups=None, subreddit=None):
    if not subreddit:
        raise Exception('please provide subreddit object')
    for submission in subreddit.submissions(start_timestamp, end_timestamp):
        if ups and submission.ups >= ups:
            yield submission

if __name__ == '__main__':
    reddit = praw.Reddit(**CREDENTIALS)

    python_subreddit = reddit.subreddit(SUBREDDIT)

    start_date = date(2017, 5, 1)
    end_date =  date(2017, 5, 30)

    start_timestamp = calendar.timegm(start_date.timetuple())
    end_timestamp = calendar.timegm(end_date.timetuple())
    link_patterns=[(re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+(:[0-9]+)?|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)'),r'\1')]
    markdown=Markdown(extras=["link-patterns"],link_patterns=link_patterns)

    # write to markdown file with links embedded
    with open('links.md', 'w') as file:
        id = 1
        for submission in get_submissions(ups=40, subreddit=python_subreddit):
            file.write(
                '  '.join(
                    [
                        str(id),
                        markdown.convert(submission.shortlink + '\n' + submission.title),
                    ]))
            id +=1
