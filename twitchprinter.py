#!/usr/bin/python
import irc.bot
import irc.strings
import time
import os
import datetime
from tprinter import *
import traceback
import imagegen
from PIL import ImageFont
import record


printer = ThermalPrinter()
admins = ['talon876']


class PrinterBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667, password=None):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.channel = channel
        printer.set_defaults()
        self.logtime = int(time.time())
        self.gen = imagegen.ImageGenerator()
        self.font_name = 'fonts/hack-bold.ttf'
        self.font_size = 24
        self.font = ImageFont.truetype(self.font_name, self.font_size)
        self.handwriting_font = ImageFont.truetype('fonts/talonscript.ttf', 32)

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

    def update_font(self, name=None, size=None):
        self.font_name = name if name is not None else self.font_name
        self.font_size = size if size is not None else self.font_size
        self.font = ImageFont.truetype(self.font_name, self.font_size)

    def handle_message(self, c, e):
        msg = e.arguments[0]
        nick = e.source.nick
        record.log_message(nick, msg)
        now = datetime.datetime.now().strftime('%c')
        log = '[{}] {}: {}'.format(now, e.source.nick, msg)
        cmd = msg.split(' ')[0].lower()
        arg = msg.replace(cmd + ' ', '')
        if cmd == 'print':
            img = self.gen.render_string(arg, self.font)
            printer.print_image(img)
        elif cmd == 'write':
            img = self.gen.render_string(arg, self.handwriting_font)
            printer.print_image(img)
        elif cmd == 'image':
            img = self.gen.render_image_code(arg)
            printer.print_image(img)
        elif cmd == 'large':
            self.update_font(size=36)
        elif cmd == 'medium':
            self.update_font(size=28)
        elif cmd == 'small':
            self.update_font(size=24)
        elif cmd == 'moar':
            if nick in admins:
                printer.linefeed(1)
        elif cmd == 'reset':
            if nick in admins:
                printer.sleep()
                printer.wake()
                printer.set_defaults()

        now = int(time.time())
        if now - self.logtime > 30 * 60:
            printer.set_defaults()
            self.logtime = now
            printer.linefeed(1)

        print(log)


def main():
    token = os.environ.get('TOKEN')
    record.init_db('twitchchat.db')
    bot = PrinterBot('#talon876', 'talon876', 'irc.chat.twitch.tv', password=token)
    bot.start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Cya')

