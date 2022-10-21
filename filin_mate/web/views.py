from itertools import chain

from django.shortcuts import get_object_or_404
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
        stats = Stat.objects.select_related(
            'type').filter(patient_id=patient_id)
        importants = stats.filter(type__important=True).distinct('type')
        notes = Note.objects.filter(patient_id=patient_id)
        stats = sorted(
            chain(stats, notes),
            key=lambda data: data.created, reverse=True)
        extra_context = {
            'importants': importants,
            'stats': stats
        }
        context.update(extra_context)
        return context
