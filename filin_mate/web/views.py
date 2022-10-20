from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from users.models import Patient
from stats.models import Stat


class PatientListView(ListView):
    model = Patient
    template_name = 'users/patient_list.html'
    context_object_name = 'patients'


class PatientDetailView(DetailView):
    model = Patient
    template_name = 'users/patient_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(Patient, id=self.kwargs['pk'])
        stats = Stat.objects.select_related('type').filter(patient=patient)
        extra_context = {'stats': stats}
        context.update(extra_context)
        return context
