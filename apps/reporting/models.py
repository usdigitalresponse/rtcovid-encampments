import uuid
from datetime import date
from datetime import timedelta

import mapbox
from django.conf import settings
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.postgres import fields as pgfields
from django.db import models
from django.urls import reverse


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Region(BaseModel):
    name = models.CharField(max_length=50)
    geom = MultiPolygonField(srid=4326)

    @classmethod
    def get_for_point(cls, pt):
        return cls.objects.get(geom__contains=pt)

    def __str__(self):
        return self.name


class Encampment(BaseModel):
    name = models.CharField(
        max_length=100,
        help_text="A descriptive name for the encampment, which may be based on the address.",
    )
    location = models.CharField(
        max_length=250,
        help_text="An intersection or address. Adding a city/state can help accuracy.",
    )
    location_geom = PointField(srid=4326)
    region = models.ForeignKey("Region", null=True, on_delete=models.PROTECT)

    def last_report(self):
        return self.reports.order_by("-date").first()

    def next_visit(self):
        return (
            ScheduledVisit.objects.filter(encampment=self, report=None)
            .order_by("-date")
            .first()
        )

    @classmethod
    def not_visited_in(cls, n_days: int):
        threshold = date.today() - timedelta(days=n_days)
        visited_encampments = [
            r.encampment.id for r in Report.objects.filter(date__gt=threshold)
        ]
        return Encampment.objects.exclude(id__in=visited_encampments)

    def get_absolute_url(self):
        return reverse("encampment-list")

    def save(self, *args, **kwargs):
        if not self.location_geom:
            # geocode
            geocoder = mapbox.Geocoder()
            result = geocoder.forward(
                self.location,
                lon=settings.LOCAL_LONGITUDE,
                lat=settings.LOCAL_LATITUDE,
            ).geojson()
            self.location_geom = GEOSGeometry(str(result["features"][0]["geometry"]))
        if not self.region:
            try:
                self.region = Region.get_for_point(self.location_geom)
            except Region.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Organization(BaseModel):
    name = models.TextField()


class ScheduledVisit(BaseModel):
    encampment = models.ForeignKey(Encampment, on_delete=models.CASCADE)
    date = models.DateField()


class Report(BaseModel):
    encampment = models.ForeignKey(
        Encampment, on_delete=models.CASCADE, related_name="reports"
    )
    performed_by = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateField()
    recorded_location = PointField(null=True, srid=4326)

    visit = models.ForeignKey(ScheduledVisit, null=True, on_delete=models.SET_NULL)

    supplies_delivered = models.TextField(blank=True)
    food_delivered = models.TextField(blank=True)
    occupancy = pgfields.IntegerRangeField(null=True)
    talked_to = models.IntegerField()
    assessed = models.IntegerField()
    assessed_asymptomatic = models.IntegerField()

    needs = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    @classmethod
    def last_n(cls, days: int):
        threshold = date.today() - timedelta(days=days)
        return Report.objects.filter(date__gt=threshold)

    def get_absolute_url(self):
        return reverse("report-list", kwargs=dict(encampment=self.encampment.id))
