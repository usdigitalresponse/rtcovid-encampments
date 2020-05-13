from django.views.generic import ListView, CreateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.reporting.models import Organization, Encampment, Report
from apps.reporting.serializers import ReportSerializer, OrganizationSerializer, EncampmentSerializer


class EncampmentListView(ListView):
    model = Encampment

# TODO: admin permissions
class EncampmentCreateView(CreateView):
    model = Encampment
    fields = ["name", "canonical_location"]

class ReportListView(ListView):
    model = Report
    def get_queryset(self):
        return Report.objects.filter(encampment=self.kwargs['encampment']).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encampment'] = Encampment.objects.get(id=self.kwargs['encampment'])
        return context


class OrganizationCreateView(CreateView):
    model = Organization
    fields = ["name"]

class ReportCreateView(CreateView):
    model = Report

    fields = [
        "date",
        "encampment",
        "recorded_location",
        "performed_by",
        "supplies_delivered",
        "food_delivered",
        "occupancy",
        "talked_to",
        "assessed",
        "assessed_asymptomatic",
        "needs",
        "notes",
    ]


# API views. Maybe delete.
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['encampment']
    ordering = ('date')

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class EncampmentViewSet(viewsets.ModelViewSet):
    queryset = Encampment.objects.all()
    serializer_class = EncampmentSerializer
