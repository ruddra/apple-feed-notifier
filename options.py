RSS_URLS = {'Django Newest': 'http://stackoverflow.com/feeds/tag?tagnames=django&sort=newest'}

try:
    from _options import *
except ImportError:
    print('No custom configuration assigned')