#!/usr/bin/env python
import os
import irc.bot
import irc.strings
import traceback
from argparse import ArgumentParser

class LurkerBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667, password=None):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.channel = channel

    def on_welcome(self, c, e):
        print('Joining channel {}'.format(self.channel))
        c.join(self.channel)

    def on_privmsg(self, c, e):
        try:
            self.handle_message(c, e)
        except Exception:
            print('Uh oh!')
            traceback.print_exc()

    def on_pubmsg(self, c, e):
        try:
            self.handle_message(c, e)
        except Exception:
            print('Uh oh!')
            traceback.print_exc()

    def handle_message(self, c, e):
        msg = e.arguments[0]
        nick = e.source.nick
        print('{}: {}'.format(nick, msg))


def main():
    ap = ArgumentParser(description='Lurk IRC channels and print out messages.')

    ap.add_argument('--channel', '-c',
            help='The channel to join')
    ap.add_argument('--nick', '-n',
            help='The nickname to use')
    ap.add_argument('--server', '-s',
            default='irc.chat.twitch.tv', help='The irc server to connect to')
    ap.add_argument('--password', '-p',
            nargs='?', default=os.environ.get('IRC_PASSWORD', None),
            help='Password for irc server. Can be set in $IRC_PASSWORD')
    args = ap.parse_args()

    if not args.channel or not args.nick:
        exit(ap.print_usage())

    bot = LurkerBot(args.channel, args.nick, args.server, password=args.password)
    try:
        bot.start()
    except KeyboardInterrupt:
        print('Cya bro!')

if __name__=='__main__':
    main()

