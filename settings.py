import re

LINK_PATTERNS = [(re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+(:[0-9]+)?|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)'),r'\1')]
SUBREDDIT = 'python'

# credentials format
"""
CREDENTIALS = {
 'client_id': '',
 'client_secret': '',
 'password': '',
 'username' : '',
 'user_agent': ''

}
"""

try:
    from local_settings import *
except ImportError:
    pass
