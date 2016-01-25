import rss_parser

parser_cls = rss_parser


class Notifier(object):
    feed_dict = dict()
    cmds = list()

    def notifier_cmd_maker(self, feed_dict=None):
        if feed_dict is None:
            feed_dict = self.feed_dict
        for key, value in feed_dict:
            cmd = 'display notification "{0}" with title "{1}" with subtitle "{2}"'.format(key, value[0], value[2])
            self.cmds.append(cmd)

    def get_notify_cmds(self):
        self.notifier_cmd_maker(self.feed_dict)
        return self.cmds


