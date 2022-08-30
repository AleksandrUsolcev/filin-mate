from rest_framework import serializers
from stats import models as stats
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


class PressureSerializer(serializers.ModelSerializer):
    class Meta:
        model = stats.Pressure
        fields = ('lower', 'upper', 'created')


class PulseSerializer(serializers.ModelSerializer):
    class Meta:
        model = stats.Pulse
        fields = ('data', 'created')


class SaturationSerializer(serializers.ModelSerializer):
    class Meta:
        model = stats.Saturation
        fields = ('data', 'created')


class BloodSugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = stats.BloodSugar
        fields = ('data', 'created')


class BodyHeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = stats.BodyHeat
        fields = ('data', 'created')


class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = stats.Weight
        fields = ('data', 'created')


class HeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = stats.Height
        fields = ('data', 'created')


class SleepTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = stats.SleepTime
        fields = ('data', 'created')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = stats.Location
        fields = ('latitude', 'longitude')
