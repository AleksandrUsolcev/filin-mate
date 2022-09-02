from django.contrib import admin

from .models import Stat, StatType


class StatAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'patient',
        'type',
        'data',
    )


class StatTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'min_value',
        'max_value',
    )


admin.site.register(Stat, StatAdmin)
admin.site.register(StatType, StatTypeAdmin)
