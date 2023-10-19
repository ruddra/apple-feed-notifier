# Python Apple Feed Notifier

AppleFeedNotifier is a simple Python application
for creating notifications in OSX from an RSS feed.

## Usage

1. Run `pip3 install -r 'requirements.txt'`

2. Now run this application using
   ```sh
   python feed_notify.py -nt 5 -ct 60 -t 'Django Latest' \
       -u 'https://stackoverflow.com/feeds/tag?tagnames=django&sort=newest'
   ```
   Obviously, change the options according to your preferences,
   especially the `-t` and `-u` option arguments.

To use from a Python script,

```python
from feed_notify import FeedNotifier

FeedNotifier(
   'https://stackoverflow.com/feeds/tag?tagnames=django&sort=newest',
   'Stack Overflow: New Django posts').watch()
```

The class is small and easy to understand, and easy to subclass
if you want to use a different notification mechanism, for example
(the AppleScript notifications this produces are rather lackluster,
and clicking them brings you to the Script Editor instead of
opening the associated URL like you would perhaps hope).


## Tutorial

Please visit
http://ruddra.com/2016/01/26/make-apple-notifications-from-rss-feed-using-python
to see how I did it.

## Feel free to contribute :)
