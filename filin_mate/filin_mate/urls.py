from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("project-admin/", admin.site.urls),
    path('', include('web.urls')),
    path('api/', include('api.urls')),
]
