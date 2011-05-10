#!/usr/bin/env python2.6
# Zeckviz IRC bot
# Copyright (C) 2011 Bruno Rahle
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from irc.actions import IrcAction, PingAction, HelpAction
from irc.mysocket import MySocket

import random
import time
import threading

class IrcBotException(Exception):
    """Base Exception class for IrcBot.
    """
    def __init__(self, message='Unknown Exception'):
        self.message = message
    def __str__(self):
        return repr(self.message)

class ReadingThread(threading.Thread):
    """Used to read the data from the socket and print it to the screen.
    TODO: make it killable.
    """
    def __init__(self, bot):
        """Initializes the thread.
        """
        super(ReadingThread, self).__init__()
        self.socket = bot.socket
        self.bot = bot

    def run(self):
        """Runs the thread.
        """
        while True:
            data = self.socket.readline()
            print data
            self.bot.parse(data)

class IrcBot(object):
    """This class represents an IrcBot. If you want to create your own, you have
    two options:
        1) extend this class.
        2) instance it and add your own actions to it.
    By default, only PingAction and HelpAction have already been added
    to it, so it won't quit too soon and some basic help is shown.
    """
    DEFAULT_ACTIONS = []
    HELP_ACTION = HelpAction

    def __init__(self, *args, **kwargs):
        """Initializes the IrcBot. The following arguments are required:
            * host - the server you want to connect to
            * port - the port on the server you want to connect to
            * nick - the nickname to use of the bot
            * identity - the identity of the bot
            * real_name - the 'real name' of the bot
            * owner - name of the owner (usually your name)
        """
        self.host = kwargs.get('host')
        self.port = kwargs.get('port', 6667)
        self.channels = kwargs.get('channels')
        self.nick = kwargs.get('nick')
        self.identity = kwargs.get('identity')
        self.real_name = kwargs.get('real_name')
        self.owner = kwargs.get('owner')

        self.socket = MySocket(self.host, self.port)
        self._actions = []
        self.add_action(PingAction(self))
        self.add_action(self.HELP_ACTION(self))
        for action in self.DEFAULT_ACTIONS:
            self.add_action(action(self))
        self._reading_thread = ReadingThread(self)
        self._reading_thread.start()
        self.connect()

    def send_message(self, where, what):
        """Sends a message what to where.
        """
        message = 'PRIVMSG {0} :{1}\n'.format(where, what)
        self._send(message)

    def _send(self, cmd):
        """Sends the command cmd to the server.
        """
        print cmd,
        self.socket.send(cmd)

    def connect(self):
        """Connect to the server. It also joins all the channels.
        """
        print 'Spajam se!'
        self._send('NICK {0}\n'.format(self.nick))
        self._send('USER {0} {1} bla: {2}\n'.format(self.identity, self.host,
                                                    self.real_name))
        time.sleep(3)
        for channel in self.channels:
            self._send('JOIN {0}\n'.format(channel))

    def parse(self, data):
        """Does all actions on every line from data it possibly can.
        """
        lines = data.split('\n')
        for line in lines:
            for action in self._actions:
                if action.check(line):
                    action.do(line)

    def add_action(self, action):
        """Adds an action to the action list. Action should extend IrcAction.
        """
        if not isinstance(action, IrcAction):
            raise IrcBotException('Expected IrcAction, but got ' +
                                  action.__class__.__name__)
        self._actions.append(action)

    def get_help(self):
        """Returns basic information about the bot."""
        msg = "My nick is {0} and my master is {1}. I operate on: {2}"
        return msg.format(self.nick, self.owner, self.channels)


def main():
    irc_bot = IrcBot(host='vilma.hsin.hr',
                     port=6667,
                     channels=['#test'],
                     nick='zecbot_beta' + str(int(random.random()*100)),
                     identity='zecbot',
                     real_name='Zec',
                     owner='brahle')


if __name__ == '__main__':
    main()

