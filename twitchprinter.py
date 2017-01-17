#!/usr/bin/python
import irc.bot
import irc.strings
import time
import datetime
from tprinter import *
import traceback
import imagegen
from PIL import ImageFont


printer = ThermalPrinter()
admins = ['talon876']


class PrinterBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667, password=None):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.channel = channel
        printer.set_defaults()
        self.logtime = int(time.time())
        self.gen = imagegen.ImageGenerator()
        self.font = ImageFont.truetype('fonts/hack-bold.ttf', 24)

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

    def append_log(self, log):
        with open('log.txt', 'a') as fd:
            fd.write('{}\n'.format(log))

    def handle_message(self, c, e):
        msg = e.arguments[0]
        now = datetime.datetime.now().strftime('%c')
        log = '[{}] {}: {}'.format(now, e.source.nick, msg)
        print(log)
        cmd = msg.split(' ')[0].lower()
        arg = msg.replace(cmd + ' ', '')
        if cmd == 'print':
            img = self.gen.render_string(arg, self.font)
            printer.print_image(img)
        if cmd == 'image':
            img = self.gen.render_image_code(arg)
            printer.print_image(img)
        elif cmd == 'moar':
            if e.source.nick in admins:
                printer.linefeed(1)
        elif cmd == 'reset':
            if e.source.nick in admins:
                printer.sleep()
                printer.wake()
                printer.set_defaults()

        self.append_log(log)
        
        now = int(time.time())
        if now - self.logtime > 30 * 60:
            printer.set_defaults()
            self.logtime = now
            printer.linefeed(1)


def main():
    token = os.environ.get('TOKEN')
    bot = PrinterBot('#talon876', 'talon876', 'irc.chat.twitch.tv', password=token)
    bot.start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Cya')

