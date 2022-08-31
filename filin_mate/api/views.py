from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from stats.models import Pressure, Stats
from users.models import Patient, User

from . import exceptions as exc
from .serializers import (PatientSerializer, PressureSerializer,
                          StatsSerializer, TokenSerializer)


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
    queryset = Patient.objects.all()
    lookup_field = 'telegram'


class StatsViewSet(ModelViewSet):
    def get_queryset(self):
        stat_type = self.request.query_params.get('type')
        telegram = self.request.query_params.get('user')
        if not stat_type:
            raise exc.MissingTypeParamException
        # elif stat_type not in exc.STATS_TYPES:
        #     raise exc.WrongTypeParamException
        if not telegram:
            raise exc.MissingUserParamException
        patient = Patient.objects.get_or_create(telegram=telegram)
        if stat_type == 'pressure':
            queryset = Pressure.objects.all().filter(patient=patient[0])
        else:
            queryset = Stats.objects.all().filter(
                patient=patient[0], type=stat_type)
        if self.request.query_params.get('last') == 'true':
            return [queryset.last()]
        return queryset.order_by('-created',)

    def get_serializer_class(self):
        stat_type = self.request.query_params.get('type')
        if stat_type == 'pressure':
            return PressureSerializer
        return StatsSerializer

    def perform_create(self, serializer):
        stat_type = self.request.query_params.get('type')
        telegram = self.request.query_params.get('user')
        patient = Patient.objects.get_or_create(telegram=telegram)
        if stat_type == 'pressure':
            serializer.save(patient=patient[0])
        serializer.save(patient=patient[0], type=stat_type)
