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


class StatViewSet(ModelViewSet):
    serializer_class = StatSerializer
    queryset = Stat.objects.all().order_by('-created')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = StatFilter
    http_method_names = ('post', 'get', 'delete', 'patch')

    def define_params(self):
        self.stat_type = self.request.query_params.get('type')
        self.patient = self.request.query_params.get('patient')
        self.available_type = StatType.objects.filter(slug=self.stat_type)
        if not self.patient:
            raise exc.MissingPatientParamException
        if not self.stat_type:
            raise exc.MissingTypeParamException
        if not self.available_type.exists():
            raise exc.WrongTypeParamException
        self.patient = Patient.objects.get_or_create(telegram=self.patient)

    def perform_create(self, serializer):
        self.define_params()
        serializer.save(patient=self.patient[0], type=self.available_type[0])

    def delete(self, request):
        self.define_params()
        queryset = Stat.objects.all().filter(
            patient=self.patient[0], type=self.available_type[0])
        if not queryset:
            raise exc.DataNotFoundException
        queryset.last().delete()
        return Response(
            {'detail': 'Последняя добавленная запись удалена'},
            status=status.HTTP_200_OK)

    def patch(self, request):
        self.define_params()
        queryset = Stat.objects.all().filter(
            patient=self.patient[0], type=self.available_type[0])
        if not queryset:
            serializer = StatSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data['data']
            Stat.objects.create(
                patient=self.patient[0],
                type=self.available_type[0],
                data=data)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
    filterset_class = LocationFilter
    search_fields = ('latitude', 'longitude')

    def perform_create(self, serializer):
        patient = self.request.query_params.get('patient')
        if not patient:
            raise exc.MissingPatientParamException
        patient = Patient.objects.get_or_create(telegram=patient)
        serializer.save(patient=patient[0])


class WeatherViewSet(ModelViewSet):
    queryset = Weather.objects.all().order_by('-created')
    serializer_class = WeatherSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('location', 'temp', 'pressure', 'humidity')
    search_fields = ('location', 'temp', 'pressure', 'humidity')
