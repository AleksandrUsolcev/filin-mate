from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    path(
        '',
        views.IndexView.as_view(),
        name='index'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'patients/',
        views.PatientListView.as_view(),
        name='patient_list'
    ),
    path(
        'patients/<int:pk>/stats',
        views.PatientFilterView.as_view(),
        name='patient_detail_filter'
    ),
    path(
        'patients/<int:pk>/',
        views.PatientDetailView.as_view(),
        name='patient_detail'
    ),
]
