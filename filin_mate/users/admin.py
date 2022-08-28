from django.contrib import admin

from .models import User


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'middle_name',
        'last_name',
        'created'
    )


admin.site.register(User, CustomUserAdmin)
