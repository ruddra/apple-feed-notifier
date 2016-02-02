import feedparser
import subprocess
import time
import sys

notification_delay = 5
check_delay = 60
title = "Ruddra Website"
rss = 'https://feedity.com/ruddra-com/VFZQWlFU.rss'

if '-nt' in sys.argv:
    notification_delay = int(sys.argv[sys.argv.index('-nt') + 1])

if '-ct' in sys.argv:
    check_delay = int(sys.argv[sys.argv.index('-ct') + 1])

if '-t' in sys.argv:
    title = sys.argv[sys.argv.index('-t') + 1]

if '-u' in sys.argv:
    rss = sys.argv[sys.argv.index('-u') + 1]

last_updated_time = None
dup_ids = list()
apple_cmd = "osascript -e '{0}'"
while True:
    d = feedparser.parse(rss)
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
                base_cmd = 'display notification "{0}" with title "{1}"'.format(_notification, title)
                cmd = apple_cmd.format(base_cmd)
                subprocess.Popen([cmd], shell=True)
                time.sleep(notification_delay)
    time.sleep(check_delay)

# python run.py -nt 5 -ct 10 -t DjangoLatest -u http://stackoverflow.com/feeds/tag\?tagnames\=django\&sort\=newest
