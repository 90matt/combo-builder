from django.contrib import admin

from .models import Game, Character, Command, Input, Combo
# Register your models here.

admin.site.register(Game)
admin.site.register(Character)
admin.site.register(Command)
admin.site.register(Input)
admin.site.register(Combo)
