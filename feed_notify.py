#!/usr/bin/env python3

"""
Display a notification on a Mac using AppleScript when an RSS/Atom feed
receives a new item.
"""

import logging
import subprocess
import time
from typing import Generator, List, Optional, Tuple

import feedparser
from feedparser.util import FeedParserDict  # for typing


logger = logging.getLogger(__name__)


class FeedNotifier:
    """
    Simple class for displaying RSS notifications on a Mac using AppleScript
    """
    def __init__(
            self,
            url: str,
            title: str,
            check_delay: float = 300.0,
            notification_delay: float = 5.0
    ) -> None:
        """
        Initialize a new RSS notifier.

        :param url:   The URL of the RSS feed
        :param title: The title to display in notifications
        :param check_delay:
                      How often to check for new updates (seconds; default 300)
        :param notification_delay:
                      How long to display a notification (seconds; default: 5)
        """
        self.url = url
        self.title = title
        self.check_delay = check_delay
        self.notification_delay = notification_delay

        self.last_updated: Optional[str] = None
        self.dup_ids: List[str] = []
        self.first_run = True

    def poll(self) -> Optional[FeedParserDict]:
        """
        Fetch latest changes from URL; return None if identical to previous,
        otherwise the new contents, as a FeedParserDict instance.
        """
        d = feedparser.parse(self.url)
        try:
            updated_time = d.feed.updated
        except AttributeError as exc:
            # This can happen when the network goes down (e.g. when your laptop
            # sleeps, or your wifi glitches); the feed dictionary is empty, and
            # the object contains a 'bozo_exception' field with the error
            if hasattr(d, 'bozo_exception') and d.bozo_exception:
                if 'syntax error' in d.bozo_exception.message:
                    # Probably an invalid URL as input
                    raise exc
                logger.info('bozo: %s',d.bozo_exception)
                return None
            raise exc
        if updated_time == self.last_updated:
            return None
        self.last_updated = updated_time
        return d

    def wait_for(self, duration: float) -> None:
        """
        Pause for the specified number of seconds.

        This is a separate method so that subclasses can override it,
        e.g. for using this module from an async loop.
        """
        time.sleep(duration)

    def new_items(self) -> Generator[Optional[Tuple[str, str]], None, None]:
        """
        Generator to continuously poll URL every self.check_delay seconds.
        Yield None if no new changes, else a tuple of two strings where the
        first is the notification text and the second is the URL,
        suitable for passing to notify()
        """
        while True:
            d = self.poll()
            if d is None:
                yield None
            else:
                for entry in d.entries:
                    _id = entry.id
                    if _id in self.dup_ids:
                        logger.info('Entry already exists')
                        break
                    _notification = entry.title.replace(
                        "'", '`').replace('"', '``')
                    logger.info(_notification)
                    self.dup_ids.append(_id)
                    if not self.first_run:
                        yield _notification, _id
                self.first_run = False
            self.wait_for(self.check_delay)

    def notify(self, message: str, url: str) -> None:
        """
        Display message with self.title for self.notification_delay seconds.

        The default implementation ignores the URL argument, but it is made
        available in case you want to create a subclass which can do something
        useful with it.
        """
        cmd = ["osascript", "-e",
               f'display notification "{message}" with title "{self.title}"']
        subprocess.run(cmd, check=True)
        self.wait_for(self.notification_delay)

    def watch(self) -> None:
        """
        Main entry point; endlessly loop and poll the RSS feed, delaying
        between attempts and displaying notifications when something new
        appears.
        """
        for item in self.new_items():
            if item is None:
                logger.info('No new feed')
            else:
                self.notify(*item)


def main() -> None:
    """
    Main entry point for command-line execution.
    """
    import sys

    loglevel = logging.INFO

    notification_delay = 5
    check_delay = 300
    title = 'Feedparser RSS example'
    rss = 'https://feedparser.readthedocs.io/en/latest/examples/rss20.xml'

    if '-h' in sys.argv or '-?' in sys.argv or '--help' in sys.argv:
        print(f'Usage: {sys.argv[0]} [-h] [-nt N] [-ct N] [-t T] [-u U] [-q]')
        sys.exit(0)

    if '-nt' in sys.argv:
        notification_delay = int(sys.argv[sys.argv.index('-nt') + 1])

    if '-ct' in sys.argv:
        check_delay = int(sys.argv[sys.argv.index('-ct') + 1])

    if '-t' in sys.argv:
        title = sys.argv[sys.argv.index('-t') + 1]

    if '-u' in sys.argv:
        rss = sys.argv[sys.argv.index('-u') + 1]

    if '-q' in sys.argv:
        loglevel = logging.WARNING

    logging.basicConfig(
        level=loglevel, format='%(asctime)s %(levelname)s %(message)s')

    FeedNotifier(rss, title, check_delay, notification_delay).watch()


if __name__ == '__main__':
    main()

# python feed_notify.py -nt 5 -ct 10 -t DjangoLatest \
#    -u 'https://stackoverflow.com/feeds/tag?tagnames=django&sort=newest'
