from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from stats import models as stats
from users.models import Patient, User

from . import exceptions as exc
from . import serializers as srl

STATS_TYPES = {
    'pulse': stats.Pulse,
    'pressure': stats.Pressure,
    'sugar': stats.BloodSugar,
    'heat': stats.BodyHeat,
    'weight': stats.Weight,
    'height': stats.Height,
    'sleep': stats.SleepTime,
    'location': stats.Location,
}

SRL_TYPES = {
    'pulse': srl.PulseSerializer,
    'pressure': srl.PressureSerializer,
    'sugar': srl.BloodSugarSerializer,
    'heat': srl.BodyHeatSerializer,
    'weight': srl.WeightSerializer,
    'height': srl.HeightSerializer,
    'sleep': srl.SleepTimeSerializer,
    'location': srl.LocationSerializer,
}


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
            raise exc.UserNotFoundException
        user = get_object_or_404(User, email=email)
        if user.check_password(password) is False:
            raise exc.InvalidPasswordException
        if not user.is_superuser:
            raise exc.TokenPermissionException
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class PatientViewSet(ModelViewSet):
    serializer_class = srl.PatientSerializer
    queryset = Patient.objects.all()
    lookup_field = 'telegram'


class StatsViewSet(ModelViewSet):
    def get_queryset(self):
        stat_type = self.request.query_params.get('type')
        telegram = self.request.query_params.get('user')
        if not stat_type:
            raise exc.MissingTypeParamException
        if not telegram:
            raise exc.MissingUserParamException
        self.model = STATS_TYPES[stat_type]
        patient = get_object_or_404(Patient, telegram=telegram)
        queryset = self.model.objects.all().filter(patient=patient)
        return queryset.order_by('-created',)

    def get_serializer_class(self):
        stat_type = self.request.query_params.get('type')
        self.serializer_class = SRL_TYPES[stat_type]
        return self.serializer_class

    def perform_create(self, serializer):
        telegram = self.request.query_params.get('user')
        patient = Patient.objects.get_or_create(telegram=telegram)
        serializer.save(patient=patient[0])
