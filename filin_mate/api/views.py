from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from stats.models import Location, Stat, Weather
from users.models import Patient, User

from . import exceptions as exc
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


class StatViewSet(ModelViewSet):
    serializer_class = StatSerializer
    queryset = Stat.objects.all().order_by('-created')
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('patient', 'patient__telegram', 'type', 'data')

    def perform_create(self, serializer):
        stat_type = self.request.query_params.get('type')
        patient = self.request.query_params.get('patient__telegram')
        if not patient:
            raise exc.MissingPatientParamException
        if not stat_type:
            raise exc.MissingTypeParamException
        patient = Patient.objects.get_or_create(telegram=patient)
        serializer.save(patient=patient[0], type=stat_type)

    def delete(self, request):
        stat_type = self.request.query_params.get('type')
        patient = self.request.query_params.get('patient__telegram')
        if not patient:
            raise exc.MissingPatientParamException
        if not stat_type:
            raise exc.MissingTypeParamException
        patient = Patient.objects.get_or_create(telegram=patient)
        queryset = Stat.objects.all().filter(
            patient=patient[0], type=stat_type)
        queryset.last().delete()
        return Response(
            {'detail': 'Последняя добавленная запись удалена'},
            status=status.HTTP_200_OK)

    def patch(self, request):
        stat_type = self.request.query_params.get('type')
        patient = self.request.query_params.get('patient__telegram')
        if not patient:
            raise exc.MissingPatientParamException
        if not stat_type:
            raise exc.MissingTypeParamException
        patient = Patient.objects.get_or_create(telegram=patient)
        queryset = Stat.objects.all().filter(
            patient=patient[0], type=stat_type)
        serializer = StatSerializer(
            queryset.last(),
            data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all().order_by('-created')
    serializer_class = LocationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('patient', 'patient__telegram',
                        'latitude', 'longitude')
    search_fields = ('patient__telegram', 'latitude', 'longitude')

    def perform_create(self, serializer):
        patient = self.request.query_params.get('patient__telegram')
        if not patient:
            raise exc.MissingPatientParamException
        patient = Patient.objects.get_or_create(telegram=patient)
        serializer.save(patient=patient[0])


class WeatherViewSet(ModelViewSet):
    queryset = Weather.objects.all().order_by('-created')
    serializer_class = WeatherSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('location', 'temp', 'pressure', 'humidity')
    search_fields = ('location__patient__telegram',
                     'location', 'temp', 'pressure', 'humidity')
