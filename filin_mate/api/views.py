from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from stats import models as stats
from users.models import Patient, User

from . import serializers as srl


class TokenViewSet(ModelViewSet):
    serializer_class = srl.TokenSerializer
    permission_classes = (AllowAny,)
    http_method_names = ('post',)

    def create(self, request, *args, **kwargs):
        serializer = srl.TokenSerializer(data=request.data)
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


class PatientViewSet(ModelViewSet):
    serializer_class = srl.PatientSerializer
    queryset = Patient.objects.all()
    lookup_field = "telegram"


class PulseViewSet(ModelViewSet):
    serializer_class = srl.PulseSerializer
    model = stats.Pulse

    def get_queryset(self):
        telegram = self.kwargs['telegram_id']
        patient = get_object_or_404(Patient, telegram=telegram)
        queryset = self.model.objects.all().filter(patient=patient)
        return queryset

    def perform_create(self, serializer):
        telegram = self.kwargs['telegram_id']
        patient = get_object_or_404(Patient, telegram=telegram)
        serializer.save(patient=patient)


class PressureViewSet(PulseViewSet):
    serializer_class = srl.PressureSerializer
    model = stats.Pressure


class SaturationViewSet(PulseViewSet):
    serializer_class = srl.SaturationSerializer
    model = stats.Saturation


class BloodSugarViewSet(PulseViewSet):
    serializer_class = srl.BloodSugarSerializer
    model = stats.BloodSugar


class BodyHeatViewSet(PulseViewSet):
    serializer_class = srl.BodyHeatSerializer
    model = stats.BodyHeat


class WeightViewSet(PulseViewSet):
    serializer_class = srl.WeightSerializer
    model = stats.Weight


class HeightViewSet(PulseViewSet):
    serializer_class = srl.HeightSerializer
    model = stats.Height


class SleepTimeViewSet(PulseViewSet):
    serializer_class = srl.SleepTimeSerializer
    model = stats.SleepTime


class LocationViewSet(PulseViewSet):
    serializer_class = srl.LocationSerializer
    model = stats.Location
