from django.contrib import admin

from .models import Location, Note, Stat, StatType, Weather


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
        'data_type'
    )


class NoteAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'patient'
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'latitude',
        'longitude'
    )


class WeatherAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'code',
        'temp',
        'pressure',
        'humidity',
    )


admin.site.register(Stat, StatAdmin)
admin.site.register(StatType, StatTypeAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Weather, WeatherAdmin)
