from django.core.management.base import BaseCommand
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User


class Command(BaseCommand):
    help = 'Get and refresh token for user'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='User email')
        parser.add_argument('password', type=str, help='User password')

    def handle(self, *args, **kwargs):
        email = kwargs['email'].lower()
        password = kwargs['password']
        if not User.objects.filter(email=email).exists():
            message = 'User not found'
            return message
        user = User.objects.get(email=email)
        if user.check_password(password) is False:
            message = 'Invalid password'
            return message
        if not user.is_superuser:
            message = 'User is not a superuser'
            return message
        token = AccessToken.for_user(user)
        user.token = token
        user.save()
        print(token)
