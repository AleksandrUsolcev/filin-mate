from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

v10 = DefaultRouter()

v10.register('patient', views.PatientViewSet, basename='patient')
v10.register(r'patient/(?P<telegram_id>\d+)/pressure',
             views.PressureViewSet, basename='pressure')
v10.register(r'patient/(?P<telegram_id>\d+)/pulse',
             views.PulseViewSet, basename='pulse')
v10.register(r'patient/(?P<telegram_id>\d+)/saturation',
             views.SaturationViewSet, basename='saturation')
v10.register(r'patient/(?P<telegram_id>\d+)/sugars',
             views.BloodSugarViewSet, basename='sugars')
v10.register(r'patient/(?P<telegram_id>\d+)/heats',
             views.BodyHeatViewSet, basename='heats')
v10.register(r'patient/(?P<telegram_id>\d+)/weight',
             views.WeightViewSet, basename='weight')
v10.register(r'patient/(?P<telegram_id>\d+)/height',
             views.HeightViewSet, basename='height')
v10.register(r'patient/(?P<telegram_id>\d+)/sleeps',
             views.SleepTimeViewSet, basename='sleeps')
v10.register(r'patient/(?P<telegram_id>\d+)/locations',
             views.LocationViewSet, basename='locations')
v10.register('get-token', views.TokenViewSet, basename='get_token')

urlpatterns = [
    path('1.0/', include(v10.urls))
]
