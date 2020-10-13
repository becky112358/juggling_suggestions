from django.contrib import admin

from .models import Difficulty, Pattern


class DifficultyInline(admin.StackedInline):
    model = Difficulty


class PatternAdmin(admin.ModelAdmin):
    inlines = [DifficultyInline]


admin.site.register(Pattern, PatternAdmin)
