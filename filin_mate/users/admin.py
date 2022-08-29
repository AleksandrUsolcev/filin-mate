from django.contrib import admin

from .models import Doctor, Patient, User


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'middle_name',
        'last_name',
        'created',
        'role'
    )


class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'age',
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
