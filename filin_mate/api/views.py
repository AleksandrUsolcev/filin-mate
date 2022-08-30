from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User, Patient

from .serializers import TokenSerializer, PatientSerializer


class TokenViewSet(ModelViewSet):
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)
    http_method_names = ('post',)

    def create(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email'].lower()
        password = serializer.validated_data['password']
        if not User.objects.filter(email=email).exists():
            return Response(
                {'not_found': 'Такого пользователя несуществует'},
                status=status.HTTP_404_NOT_FOUND
            )
        user = get_object_or_404(User, email=email)
        if user.check_password(password) is False:
            return Response(
                {'bad_request': 'Неверный пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not user.is_superuser:
            return Response(
                {'forbidden': 'Нет прав для получения токена'},
                status=status.HTTP_403_FORBIDDEN
            )
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class PatientSerializer(ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
