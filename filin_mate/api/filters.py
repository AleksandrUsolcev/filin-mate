import django_filters
from stats.models import Location, Note, Stat


class StatFilter(django_filters.FilterSet):
    patient = django_filters.NumberFilter(field_name='patient__telegram')
    type = django_filters.CharFilter(field_name='type__slug')

    class Meta:
        model = Stat
        fields = '__all__'


class NoteFilter(django_filters.FilterSet):
    patient = django_filters.NumberFilter(field_name='patient__telegram')

    class Meta:
        model = Note
        fields = '__all__'


class LocationFilter(django_filters.FilterSet):
    patient = django_filters.NumberFilter(field_name='patient__telegram')

    class Meta:
        model = Location
        fields = '__all__'
