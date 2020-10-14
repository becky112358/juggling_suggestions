from django.contrib import admin

from .models import Difficulty, Modifier, Pattern


# class BodyThrowInline(admin.TabularInline):
#     model = BodyThrow
#     extra = 1
#
#
#
class ModifierInline(admin.StackedInline):
    model = Modifier
    classes = ['collapse']


class DifficultyInline(admin.StackedInline):
    model = Difficulty


class PatternAdmin(admin.ModelAdmin):
    inlines = [ModifierInline,
               DifficultyInline]


admin.site.register(Pattern, PatternAdmin)
