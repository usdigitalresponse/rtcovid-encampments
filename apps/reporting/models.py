import uuid

from django.contrib.gis.db.models import PointField
from django.contrib.postgres import fields as pgfields
from django.db import models

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Encampment(BaseModel):
    name = models.TextField()

class Organization(BaseModel):
    name = models.TextField()

class ScheduledVisit(BaseModel):
    encampment = models.ForeignKey(Encampment, on_delete=models.CASCADE)
    date = models.DateField()

class Visit(BaseModel):
    encampment = models.ForeignKey(Encampment, on_delete=models.CASCADE)
    performed_by = models.ForeignKey(Organization, on_delete=models.CASCADE)

    date = models.DateField()
    recorded_location = PointField()
    supplies_delivered = models.TextField(blank=True)
    food_delivered = models.TextField(blank=True)
    occupancy = pgfields.IntegerRangeField(null=True)
    talked_to = models.IntegerField()
    assessed = models.IntegerField()
    assessed_asymptomatic = models.IntegerField()

    needs = models.TextField()
    notes = models.TextField()
