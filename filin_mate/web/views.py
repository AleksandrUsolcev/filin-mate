from itertools import chain

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
        patient_id = self.kwargs['pk']
        self.stats = Stat.objects.select_related(
            'type').filter(patient_id=patient_id)
        importants = self.stats.filter(type__important=True).distinct('type')
        types = self.stats.distinct('type')
        notes = Note.objects.filter(patient_id=patient_id)
        stats = sorted(
            chain(self.stats, notes),
            key=lambda data: data.created, reverse=True)
        extra_context = {
            'types': types,
            'importants': importants,
            'stats': stats,
            'checked_all': True
        }
        context.update(extra_context)
        return context


class PatientFilterView(PatientDetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_id = self.kwargs['pk']
        stats = self.stats.filter(type__in=self.request.GET.getlist('type'))
        notes = Note.objects.filter(patient_id=patient_id)
        checked = stats.values_list('type', flat=True).distinct()
        stats = sorted(
            chain(stats, notes),
            key=lambda data: data.created, reverse=True)
        extra_context = {
            'stats': stats,
            'checked': checked,
            'checked_all': False
        }
        context.update(extra_context)
        return context
