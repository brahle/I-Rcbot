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

from irc.ircbot import IrcBot
from spoilbot.models import SpoilerBot
from django.core.exceptions import MiddlewareNotUsed

import random

class IrcMiddleware(object):
    """This sucks big time! If you want to start the bot, after you start the
    server, you need to visit the website. 
    """
    def __init__(self):
        """Creates the IrcBot and reports that the bot is not used. 
        """
        try:
            self.bots
        except AttributeError:
            self.bots = [
                SpoilerBot(
                    host='vilma.hsin.hr',
                    port=6667,
                    channels=['#zadaci'],
                    nick='SpoilerBot',
                    identity='SpoilerBot',
                    real_name='I like to spoil things!',
                    owner='brahle'),
                ]
        raise MiddlewareNotUsed()

def main():
    StartMiddleware()


if __name__ == '__main__':
    main()

