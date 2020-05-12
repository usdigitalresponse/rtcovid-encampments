from rest_framework import viewsets

from apps.reporting.models import Visit, Organization, Encampment
from apps.reporting.serializers import VisitSerializer, OrganizationSerializer, EncampmentSerializer


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class EncampmentViewSet(viewsets.ModelViewSet):
    queryset = Encampment.objects.all()
    serializer_class = EncampmentSerializer
