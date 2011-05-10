from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from irc.ircbot import IrcBot
from irc.actions import KeywordAction

class Spoiler(models.Model):
    author = models.CharField(max_length=255)
    text = models.CharField(max_length=1023)


class SpoilAction(KeywordAction):
    AUTHOR = 'brahle'
    KEYWORD = '!spoil'
    DESCRIPTION = """Use this to spoil a message. Usage: /msg {name} !spoil \
text-to-spoil"""
    def _do(self):
        spoiler = Spoiler(author=self.sender, text=self.message)
        spoiler.save()
        msg = 'User {0} created spoiler {1}!'
        notification = msg.format(self.sender, spoiler.id)
        if self.channel not in self.bot.channels:
            self.bot.send_message(self.channel, notification)
        for channel in self.bot.channels:
            self.bot.send_message(channel, notification)


class UnspoilAction(KeywordAction):
    AUTHOR = 'brahle'
    KEYWORD = '!unspoil'
    DESCRIPTION = """Unspoils the message hidden behind the given id. Usage: \
!unspoil <id>"""
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


class SpoilerBot(IrcBot):
    DEFAULT_ACTIONS = [SpoilAction, UnspoilAction]
