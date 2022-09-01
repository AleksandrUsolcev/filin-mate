from rest_framework import serializers
from stats.models import Stat
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
    type = serializers.CharField(required=False)
    patient = serializers.SlugRelatedField(
        slug_field='telegram',
        read_only=True
    )

    class Meta:
        model = Stat
        fields = ('patient', 'data', 'type', 'created')
