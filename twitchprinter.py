#!/usr/bin/python
import irc.bot
import irc.strings
import os
import time
import datetime
from tprinter import *
import traceback

printer = ThermalPrinter('/dev/serial0', 19200, timeout=5)

class PrinterBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667, password=None):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.channel = channel
        self.bold = False
        printer.sleep()
        printer.wake()
        printer.setDefault()
        self.logtime = int(time.time())
        #printer.println('Joining {}'.format(self.channel))
        #printer.println(datetime.datetime.now().strftime('%c'))

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
            printer.println(arg)
        if cmd == 'append' or cmd == 'write':
            printer._print(arg)
        elif cmd == 'left':
            printer.justify('L')
        elif cmd == 'right':
            printer.justify('R')
        elif cmd == 'center':
            printer.justify('C')
        elif cmd == 'moar':
            if e.source.nick == 'talon876':
                printer.feed(1)
        elif cmd == 'large':
            printer.setSize('L')
        elif cmd == 'medium':
            printer.setSize('M')
        elif cmd == 'small':
            printer.setSize('S')
        elif cmd == 'reset':
            printer.sleep()
            printer.wake()
            printer.setDefault()
        elif cmd == 'bold':
            if self.bold:
                printer.boldOn()
            else:
                printer.boldOff()
            self.bold = not self.bold

        self.append_log(log)
        
        now = int(time.time())
        if now - self.logtime > 30 * 60:
            printer.setDefault()
            #printer.println(datetime.datetime.now().strftime('%c'))
            self.logtime = now
            printer.feed(1)
            

def main():
    token = os.environ.get('TOKEN')
    bot = PrinterBot('#talon876', 'talon876', 'irc.chat.twitch.tv', password=token)
    bot.start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Cya')

