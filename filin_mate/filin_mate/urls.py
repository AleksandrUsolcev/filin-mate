from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("project-admin/", admin.site.urls),
    path('', include('web.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
