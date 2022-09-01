from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

v10 = DefaultRouter()

v10.register('patients', views.PatientViewSet, basename='patients')
v10.register('get-token', views.TokenViewSet, basename='get_token')
v10.register('stats', views.StatViewSet, basename='stats')

urlpatterns = [
    path('1.0/', include(v10.urls))
]
