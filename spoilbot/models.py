from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from irc.ircbot import IrcBot
from irc.actions import KeywordAction

class Spoiler(models.Model):
    author = models.CharField(max_length=255)
    text = models.CharField(max_length=1023)


class SpoilAction(KeywordAction):
    KEYWORD = '!spoil'
    def _do(self):
        spoiler = Spoiler(author=self.sender, text=self.message)
        spoiler.save()
        notification = '{0} created spoiler {1}!'.format(self.sender, spoiler.id)
        if self.channel not in self.bot.channels:
            self.bot.send_message(self.channel, notification)
        for channel in self.bot.channels:
            self.bot.send_message(channel, notification)
        

class UnspoilAction(KeywordAction):
    KEYWORD = '!unspoil'
    def _do(self):
        try:
            spoiler_id = int(self.message)
            spoiler = Spoiler.objects.get(id=spoiler_id)
        except ValueError:
            error = 'I don\'t know what to do with "{0}"!'.format(self.message)
            self.bot.send_message(self.channel, error)
            return
        except ObjectDoesNotExist:
            error = 'Unknown spoiler id ({0})!'.format(spoiler_id)
            self.bot.send_message(self.channel, error)
            return
        self.bot.send_message(self.sender, spoiler.text)


class SpoilHelpAction(KeywordAction):
    KEYWORD = '!spoil-help'
    def _do(self):
        help_string = '{0} currently supports two options: "/msg {0} {1} text to spoil" and "{2} <id>"'
        response = help_string.format(self.bot.nick, SpoilAction.KEYWORD,
                                      UnspoilAction.KEYWORD)
        self.bot.send_message(self.channel, response)

class SpoilerBot(IrcBot):
    DEFAULT_ACTIONS = [SpoilAction, UnspoilAction, SpoilHelpAction]
