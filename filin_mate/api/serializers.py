from rest_framework import serializers
from stats.models import Pressure, Stats
from users.models import Patient, User


class TokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password')


class PatientSerializer(serializers.ModelSerializer):
    telegram = serializers.IntegerField(required=True)

    class Meta:
        model = Patient
        fields = ('telegram', 'user', 'age')


class StatsSerializer(serializers.ModelSerializer):
    type = serializers.CharField(required=False)

    class Meta:
        model = Stats
        fields = ('data', 'type', 'created')


class PressureSerializer(serializers.ModelSerializer):
    type = serializers.CharField(required=False, default='pressure')

    class Meta:
        model = Pressure
        fields = ('upper', 'lower', 'type', 'created')
