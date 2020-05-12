from drf_extra_fields.fields import IntegerRangeField
from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from apps.reporting.models import Visit, Organization, Encampment


class VisitSerializer(serializers.ModelSerializer):
    recorded_location = PointField()
    occupancy = IntegerRangeField()
    class Meta:
        model = Visit
        fields = [
            "date",
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