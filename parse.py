from datetime import datetime, date
import calendar
from pprint import pprint

import praw



def get_submissions(score=None, ups=None, subreddit=None):
    if not subreddit:
        raise Exception('please provide subreddit object')
    for submission in subreddit.submissions(start_timestamp, end_timestamp):
        if ups:
            if submission.ups >= ups:
                yield submission

def construct_full_url(submission):
    return '/'.join(['https://www.reddit.com', submission.permalink])

if __name__ == '__main__':
    reddit = praw.Reddit(client_id="", client_secret="",
                         password='', user_agent='USERAGENT',
                         username='')

    python_subreddit = reddit.subreddit('python')

    start_date = date(2017, 5, 20)
    end_date =  date(2017, 5, 30)

    start_timestamp = calendar.timegm(start_date.timetuple())
    end_timestamp = calendar.timegm(end_date.timetuple())


    for submission in get_submissions(ups=40, subreddit=python_subreddit):
        print(submission.ups, submission.title, submission.shortlink)

# for topic in reddit.subreddit('python').hot():
#     print(topic)
