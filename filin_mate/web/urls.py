from django.contrib.auth.views import LoginView
from django.urls import path

app_name = 'web'

urlpatterns = [
    path(
        '',
        LoginView.as_view(template_name='main/index.html'),
        name='index'
    ),
]
