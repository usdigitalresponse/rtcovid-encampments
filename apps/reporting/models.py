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
from django.urls import reverse_lazy as reverse
from django.utils import timezone
from django.utils.text import slugify


DELAY_THRESHOLD_DAYS = 14


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Region(BaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    geom = MultiPolygonField(srid=4326)

    @classmethod
    def get_for_point(cls, pt):
        return cls.objects.get(geom__contains=pt)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("region-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class EncampmentManager(models.Manager):
    def tasked(self, **kwargs):
        return self.filter(tasks__completed=None).exclude(tasks__isnull=True).distinct()

    def delayed(self, days=DELAY_THRESHOLD_DAYS, **kwargs):
        threshold = date.today() - timedelta(days=days)
        visited_encampments = [
            r.encampment.id for r in Report.objects.filter(date__gt=threshold)
        ]
        return self.exclude(id__in=visited_encampments)


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

    def open_tasks(self):
        return self.tasks.filter(completed=None)

    def completed_tasks(self):
        return self.tasks.exclude(completed=None)

    def reports(self):
        return self.reports.order_by("-date")

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
        return Encampment.objects.delayed(days=n_days)

    def get_absolute_url(self):
        return reverse("encampment-detail", kwargs={"pk": self.id})

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
            self.region = Region.get_for_point(self.location_geom)
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.name, self.location)

    objects = EncampmentManager()

    class Meta:
        ordering = ("name",)


class Organization(BaseModel):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(
        "auth.User", related_name="organizations", blank=True
    )

    def __str__(self):
        return self.name


class Task(BaseModel):
    title = models.CharField(max_length=512)
    details = models.TextField(blank=True)
    encampment = models.ForeignKey(
        Encampment, on_delete=models.CASCADE, related_name="tasks"
    )

    completed = models.DateTimeField(null=True)

    def get_absolute_url(self):
        return reverse("encampment-detail", kwargs={"pk": self.encampment.id})

    def mark_completed(self):
        self.completed = timezone.now()
        self.save()


class ScheduledVisit(BaseModel):
    encampment = models.ForeignKey(Encampment, on_delete=models.CASCADE)
    date = models.DateField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("encampment-detail", kwargs={"pk": self.encampment.id})


class Report(BaseModel):
    encampment = models.ForeignKey(
        Encampment, on_delete=models.CASCADE, related_name="reports"
    )

    type_of_setup = models.CharField(max_length=100, help_text="Tents, vehicles, etc.")
    performed_by = models.ForeignKey(
        Organization, on_delete=models.CASCADE, verbose_name="Visiting Organization"
    )
    date = models.DateField(verbose_name="Date Visited")
    recorded_location = PointField(null=True, srid=4326)

    visit = models.ForeignKey(ScheduledVisit, null=True, on_delete=models.SET_NULL)

    supplies_delivered = models.TextField(
        blank=True, help_text="Specify items & quantity"
    )
    food_delivered = models.TextField(blank=True, help_text="Specify items & quantity")
    occupancy = pgfields.IntegerRangeField(null=True, verbose_name="People Living Here")

    talked_to = models.IntegerField(verbose_name="People Talked To")
    assessed = models.IntegerField(verbose_name="People Assessed for COVID")
    assessed_asymptomatic = models.IntegerField(
        verbose_name="People Assessed for COVID and Asymptomatic"
    )
    # Looking through the sheet, we probably to suggest "verbal", "flyer", "none", "declined" but allow free text
    # if neither fits.
    education_provided = models.CharField(
        max_length=100, verbose_name="COVID Education Provided"
    )

    needs = models.TextField(blank=True, verbose_name="Outstanding Needs")
    notes = models.TextField(blank=True, verbose_name="Other Notes")

    @classmethod
    def last_n(cls, days: int):
        threshold = date.today() - timedelta(days=days)
        return Report.objects.filter(date__gt=threshold)

    def get_absolute_url(self):
        return reverse("encampment-detail", kwargs=dict(pk=self.encampment.id))
