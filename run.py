import feedparser
import subprocess
# import Foundation
import time

from options import RSS_URL, RSS_TITLE, NOTIFICATION_DELAY, CHECK_DELAY


rss_url = RSS_URL
rss_title = RSS_TITLE

last_updated_time = None
dup_ids = list()
apple_cmd = "osascript -e '{0}'"
while True:
    d = feedparser.parse(rss_url)
    updated_time = d.feed.updated
    if updated_time == last_updated_time:
        print('No new feed')
    else:
        last_updated_time = updated_time
        for entry in d.entries:
            _id = entry.id
            _notification = entry.title.replace("'", '`').replace('"', '``')
            if _id in dup_ids:
                print('Entry already exists, ')
                break
            else:
                print(_notification)
                dup_ids.append(_id)
                base_cmd = 'display notification "{0}" with title "{1}"'.format(_notification, rss_title)
                cmd = apple_cmd.format(base_cmd)
                subprocess.Popen([cmd], shell=True)
                time.sleep(NOTIFICATION_DELAY)
    time.sleep(CHECK_DELAY)


