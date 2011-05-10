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

import random

class IrcAction(object):
    """Base class for IRC interaction.

    This class is used to trigger an action. When a line of text is
    received, it is then parsed by the ``check()`` method. If
    ``check()`` returns ``True``, ``do`` method is invoked with the
    same line of text as the parameter.

    Attributes:
        * bot: the IRC bot this class is atteched to
        * AUTHOR: a string identifying the author of the action
        * DESCRIPTION: a short text that is displayed when help is invoked
        * IN_HELP: a boolean flag indicationg should it be displayed in help
    """

    AUTHOR = None
    DESCRIPTION = 'I have no clue what this command does!'
    IN_HELP = False
    def __init__(self, bot):
        """Initializer that attaches the bot to the action.

        Args:
            * bot: the bot that has this particular action attached.
        """
        self.bot = bot

    def check(self, line):
        """Checks if this action was triggered by the last line of text.

        Args:
            * line: The line of text received from IRC.

        Returns:
            If this line is relevant for this action, it returns `True`.
            Otherwise, it returns `False`.
        """
        return False

    def do(self, line):
        """Performs the action required by the bot.

        Args:
            * line: The line of text received from IRC.
        """
        pass

    def _is_privmsg(self, line):
        """Checks if the message received is a PRIVMSG."""
        parts = line.strip().split(' ')
        return parts[1] == 'PRIVMSG'

    def _get_message(self, line):
        """Returns the message part of the PRIVMSG."""
        parts = line.strip().split(':')[2:]
        return ':'.join(parts)

    def _get_channel(self, line):
        """Returns the channel where PRIVMSG was received."""
        parts = line.strip().split(' ')
        if parts[2] == self.bot.nick:
            return self._get_sender(line)
        return parts[2]

    def _get_sender(self, line):
        """Returns the sender of the message."""
        sender = line[line.find(':')+1:line.find('!')]
        return sender

    def get_help(self):
        """Returns the help text for this action."""
        return self.DESCRIPTION


class PingAction(IrcAction):
    """Used to the ping communaction with the IRC server."""
    # TODO (brahle) answer to user ping requests
    AUTHOR = 'brahle'
    DESCRIPTION = 'Keepalive with the IRC server.'
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
    """Action that repeats what you just said."""
    AUTHOR = 'brahle'
    DESCRIPTION = 'Echoes your last words.'
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
    IN_HELP = True
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
        """Called at the end of the ``do()`` method."""
        pass

    def get_help(self):
        """Returns the help text, formatted as 'keyword': description."""
        msg = "'{0}': {1}"
        return msg.format(self.KEYWORD, self.DESCRIPTION)


class HelpAction(KeywordAction):
    """Action that prints the help."""
    AUTHOR = 'brahle'
    KEYWORD = '?help'
    DESCRIPTION = 'Prints this help message.'
    IN_HELP = False
    def _do(self):
        info = self.bot.get_help()
        self.bot.send_message(self.channel, info)
        self.bot.send_message(self.channel, "The commands I adhere to are:")
        printed = False
        for action in self.bot._actions:
            text = '\t' + action.get_help().format(name=self.bot.nick)
            if action.IN_HELP:
                self.bot.send_message(self.channel, text)
                printed = True
        if not printed:
            messages = [
                "Scratch that, you are not the boss of me!!!",
                "It's not gonna be that easy, will it?",
                "Welcome to Clowntown! Population: You.",
                "I'm a pretty useless bot, I don't do a thing."
            ]
            self.bot.send_message(self.channel, random.choice(messages))
