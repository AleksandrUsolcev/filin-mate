import csv
from itertools import chain

from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from stats.models import Note, Stat
from users.models import Patient


class PatientListView(ListView):
    model = Patient
    template_name = 'users/patient_list.html'
    context_object_name = 'patients'


class PatientDetailView(DetailView):
    model = Patient
    template_name = 'users/patient_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_id = self.kwargs.get('pk')
        self.stats = Stat.objects.select_related(
            'type').filter(patient_id=patient_id)
        importants = self.stats.filter(type__important=True).distinct('type')
        types = self.stats.distinct('type')
        self.notes = Note.objects.filter(patient_id=patient_id)
        stats = sorted(
            chain(self.stats, self.notes),
            key=lambda data: data.created, reverse=True)
        extra_context = {
            'types': types,
            'importants': importants,
            'stats': stats
        }
        context.update(extra_context)
        return context


class PatientFilterView(PatientDetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered = True
        notes_status = True
        if not self.request.GET.getlist('notes'):
            self.notes = []
            notes_status = False
        stats = self.stats.filter(type__in=self.request.GET.getlist('t'))
        checked = stats.values_list('type', flat=True).distinct()
        stats = sorted(
            chain(stats, self.notes),
            key=lambda data: data.created, reverse=True)
        extra_context = {
            'stats': stats,
            'checked': checked,
            'filtered': filtered,
            'notes_status': notes_status
        }
        context.update(extra_context)
        return context

    def get(self, request, *args, **kwargs):
        if self.request.GET.getlist('export-csv'):
            types = self.request.GET.getlist('t')
            patient_id = self.kwargs.get('pk')
            response = HttpResponse(content_type='text/csv')
            stats = Stat.objects.select_related('type').filter(
                patient=patient_id, type__in=types).order_by('-created').values_list(
                'created', 'patient__id', 'type__name', 'data')
            writer = csv.writer(response)
            writer.writerow(
                ['Добавлено', 'id пациента', 'Тип данных', 'Показатели'])
            for stat in stats:
                writer.writerow(stat)
            response['Content-Disposition'] = 'attachment; filename="stats.csv"'
            return response
        return super().get(request)
