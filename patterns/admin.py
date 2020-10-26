from django.contrib import admin

from .models import BodyThrow, Modifier, Pattern


class BodyThrowInline(admin.TabularInline):
    model = BodyThrow
    extra = 1


class ModifierInline(admin.StackedInline):
    model = Modifier
    classes = ['collapse']


class PatternAdmin(admin.ModelAdmin):
    inlines = [BodyThrowInline,
               ModifierInline,
               ]


admin.site.register(Pattern, PatternAdmin)
