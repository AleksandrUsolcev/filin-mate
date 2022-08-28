from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("project-admin/", admin.site.urls),
    path('', include('users.urls')),
    path('', include('stats.urls')),
    path('api/', include('api.urls')),
]
