import argparse
import datetime

from reddit_parser import RedditParser

try:
    from settings import CREDENTIALS, SUBREDDIT
except ImportError:
    raise Exception('please define variables in your settings file.')


def date_action():
    class DateAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            setattr(args, self.dest, parse_dates(values))
    return DateAction


def parse_dates(value):
    return int(datetime.datetime.strptime(value,  '%Y-%m-%d').timestamp())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve Reddit posts and stores them as html file with links.')
    parser.add_argument("--start", help='date from which submissions will be searched.', action=date_action())
    parser.add_argument("--end", help='date until which submissions will be searched.', action=date_action())
    parser.add_argument("--ups", type=int,
                        help='minimal upvotes which submission should have to be included into result.')
    parser.add_argument("--limit", required=False, default=None, type=int,
                        help='max number of records that should be included into result.')

    args = parser.parse_args()

    RedditParser().parse(ups=args.ups, start=args.start, end=args.end, limit=args.limit)



