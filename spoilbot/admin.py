from django.contrib import admin
from spoilbot.models import Spoiler

class SpoilerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Spoiler, SpoilerAdmin)
