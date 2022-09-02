from django.contrib import admin
from .models import Stat


class StatAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'patient',
        'type',
        'data',
    )


admin.site.register(Stat, StatAdmin)
