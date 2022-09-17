from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from stats.models import Location, Stat, StatType, Weather
from users.models import Patient, User

from . import exceptions as exc
from .filters import LocationFilter, StatFilter
from .serializers import (LocationSerializer, PatientSerializer,
                          StatSerializer, TokenSerializer, WeatherSerializer)


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
            raise exc.UserNotFoundException
        user = get_object_or_404(User, email=email)
        if user.check_password(password) is False:
            raise exc.InvalidPasswordException
        if not user.is_superuser:
            raise exc.TokenPermissionException
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class PatientViewSet(ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all().order_by('-created')
    lookup_field = 'telegram'
    filterset_fields = ('telegram', 'age')
    search_fields = ('telegram', 'age')

    def get_queryset(self):
        telegram = self.request.query_params.get('telegram')
        if telegram:
            telegram = Patient.objects.filter(telegram=telegram)
            if not telegram.exists():
                raise exc.UserNotFoundException
        return super().get_queryset()


class StatViewSet(ModelViewSet):
    serializer_class = StatSerializer
    queryset = Stat.objects.all().order_by('-created')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = StatFilter
    http_method_names = ('post', 'get', 'delete', 'patch')

    def get_queryset(self):
        stat_type = self.request.query_params.get('type')
        patient = self.request.query_params.get('patient')
        if patient:
            patient = Patient.objects.filter(telegram=patient)
            if not patient.exists():
                raise exc.UserNotFoundException
        if stat_type:
            stat_type = StatType.objects.filter(slug=stat_type)
            if not stat_type.exists():
                raise exc.WrongTypeParamException
        return super().get_queryset()


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all().order_by('-created')
    serializer_class = LocationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = LocationFilter
    search_fields = ('latitude', 'longitude')


class WeatherViewSet(ModelViewSet):
    queryset = Weather.objects.all().order_by('-created')
    serializer_class = WeatherSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('location', 'temp', 'pressure', 'humidity')
    search_fields = ('location', 'temp', 'pressure', 'humidity')
