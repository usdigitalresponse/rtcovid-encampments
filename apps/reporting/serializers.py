from drf_extra_fields.fields import IntegerRangeField
from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from apps.reporting.models import Encampment
from apps.reporting.models import Organization
from apps.reporting.models import Report


class ReportSerializer(serializers.ModelSerializer):
    recorded_location = PointField()
    occupancy = IntegerRangeField()

    class Meta:
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


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["name"]


class EncampmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encampment
        fields = ["name"]
