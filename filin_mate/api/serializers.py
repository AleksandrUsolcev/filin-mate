from rest_framework import serializers
from stats.models import Location, Note, Stat, StatType, Weather
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
        fields = ('id', 'telegram', 'user', 'age', 'created')


class StatSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=StatType.objects.all()
    )
    patient = serializers.SlugRelatedField(
        slug_field='telegram',
        queryset=Patient.objects.all()
    )

    class Meta:
        model = Stat
        fields = ('id', 'patient', 'data', 'type', 'created')


class NoteSerializer(serializers.ModelSerializer):
    patient = serializers.SlugRelatedField(
        slug_field='telegram',
        queryset=Patient.objects.all()
    )

    class Meta:
        model = Note
        fields = ('id', 'patient', 'text')


class LocationSerializer(serializers.ModelSerializer):
    patient = serializers.SlugRelatedField(
        slug_field='telegram',
        read_only=True
    )

    class Meta:
        model = Location
        fields = '__all__'


class WeatherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Weather
        fields = '__all__'
