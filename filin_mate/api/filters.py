import django_filters
from stats.models import Location, Stat


class StatFilter(django_filters.FilterSet):
    patient = django_filters.NumberFilter(field_name='patient__telegram')

    class Meta:
        model = Stat
        fields = '__all__'


class LocationFilter(django_filters.FilterSet):
    patient = django_filters.NumberFilter(field_name='patient__telegram')

    class Meta:
        model = Location
        fields = '__all__'
