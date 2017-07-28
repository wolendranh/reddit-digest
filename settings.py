
SUBREDDIT = 'python'

# credentials format
"""
CREDENTIALS = {
 'client_id': ',
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
