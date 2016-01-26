RSS_URL = 'http://stackoverflow.com/feeds/tag?tagnames=django&sort=newest'
RSS_TITLE = "Django Latest"
NOTIFICATION_DELAY = 5  # seconds
CHECK_DELAY = 60  # seconds

try:
    from _options import *
except ImportError:
    print('No custom configuration assigned')