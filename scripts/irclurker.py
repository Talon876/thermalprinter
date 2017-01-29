#!/usr/bin/env python
import os
import irc.bot
import irc.strings
import traceback

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
    token = os.environ.get('IRC_PASSWORD')
    bot = LurkerBot('#talon876', 'talon876', 'irc.chat.twitch.tv', password=token)
    bot.start()

if __name__=='__main__':
    main()

