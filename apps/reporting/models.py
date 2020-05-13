import uuid

from django.contrib.gis.db.models import PointField
from django.contrib.postgres import fields as pgfields
from django.db import models
from django.urls import reverse


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Encampment(BaseModel):
    name = models.TextField()
    canonical_location = PointField(srid=4326)
    def get_absolute_url(self):
        return reverse('encampment-list')

class Organization(BaseModel):
    name = models.TextField()

class ScheduledVisit(BaseModel):
    encampment = models.ForeignKey(Encampment, on_delete=models.CASCADE)
    date = models.DateField()

class Report(BaseModel):
    encampment = models.ForeignKey(Encampment, on_delete=models.CASCADE)
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

    def get_absolute_url(self):
        return reverse('report-list', kwargs=dict(encampment=self.encampment.id))

