import feedparser
from options import RSS_URLS
import time

feed_module = feedparser

last_updated = None
while True:
    for urls in RSS_URLS:
        d = feedparser.parse(urls)
        parser_updated_time = d.feed.updated
        if parser_updated_time != last_updated:
            print('Feed Updated')
            last_updated = parser_updated_time

        print(parser_updated_time)
        for entry in d.entries:
            pass
            # print(entry.title)
            # print(entry.id)
        time.sleep(5)


class RSSParserModule(object):
    parser_dict = dict()

    def parse_feed(self, _url, feed_class=feed_module):
        return feed_class.parse(_url)

    def parse_urls(self, rss_urls=RSS_URLS):
        for key, value in rss_urls.items():
            self.parser_dict[key] = self.parse_feed(value)

    def get_feed_dict(self, url_conf):
        self.parse_urls(url_conf)
        return self.parser_dict

