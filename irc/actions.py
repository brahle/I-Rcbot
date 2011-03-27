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

class IrcAction(object):
    """This class is used to do trigger an action. When a line is received,
    you need to parse it.
    """
    def __init__(self, bot):
        self.bot = bot

    def check(self, line):
        """Checks if the current line is the one that requires that this action
        is peroformed upon it.
        """
        return False

    def do(self, line):
        """Does the required action.
        """
        pass

    def _is_privmsg(self, line):
        """Checks if the message received is a PRIVMSG.
        """
        parts = line.strip().split(' ')
        return parts[1] == 'PRIVMSG'

    def _get_message(self, line):
        """Returns the message part of the PRIVMSG.
        """
        parts = line.strip().split(':')[2:]
        return ':'.join(parts)

    def _get_channel(self, line):
        """Returns the channel where PRIVMSG was received.
        """
        parts = line.strip().split(' ')
        if parts[2] == self.bot.nick:
            return self._get_sender(line)
        return parts[2]

    def _get_sender(self, line):
        """Returns the sender of the message.
        """
        sender = line[line.find(':')+1:line.find('!')]
        return sender


class PingAction(IrcAction):
    """Used to the ping communaction with the IRC server.
    """
    def check(self, line):
        """Checks if the ping request is received.
        """
        parts = line.strip().split(' ')
        return parts[0] == 'PING'

    def do(self, line):
        """Responds with pong.
        """
        parts = line.strip().split(' ')
        self.bot._send('PONG ' + parts[1] + '\n')


class EchoAction(IrcAction):
    """Repeats what you just said. Great for debugging.
    """
    def check(self, line):
        """Checks if the current line is a privmsg."""
        return self._is_privmsg(line)

    def do(self, line):
        """Echo the last message received using the same channel."""
        channel = self._get_channel(line)
        message_received = self._get_message(line)
        self.bot.send_message(channel, message_received)


class KeywordAction(IrcAction):
    """Extend this class if you want to add a command to the bot. It is just a
    utility class as, it only implements a method to check if the received
    message starts with self.KEYWORD. The deafult do method will save you some
    work by automatically saving the sender, message and channel data. 
    """
    KEYWORD = None      # put a keyword string, like '!start' when you extend it

    def check(self, line):
        """Checks if the message starts with self.KEYWORD
        """
        if not self._is_privmsg(line):
            return False
        message = self._get_message(line).split()
        return message[0] == self.KEYWORD

    def do(self, line):
        """Saves message, sender, and channel data and calls _do() method.
        """
        self.message = self._get_message(line)[len(self.KEYWORD)+1:].strip()
        self.sender = self._get_sender(line)
        self.channel = self._get_channel(line)
        self._do()

    def _do(self):
        """It is called at the end of do() method. 
        """
        pass

