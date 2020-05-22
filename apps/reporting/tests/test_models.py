from datetime import date
from datetime import timedelta

from django.contrib.gis.geos import Point
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from apps.reporting import models as app_models
from apps.reporting.models import Organization
from apps.reporting.models import ScheduledVisit


class TestModels(TestCase):
    def setUp(self):
        call_command("preload_oakland")
        self.org = Organization.objects.create(name="test org")

    def test_region(self):
        points = [
            (Point(-122.2943896, 37.8051279), "District 3"),
            (Point(-122.2245076, 37.7777988), "District 5"),
            (Point(-122.44994547, 37.76389937), None),
        ]
        for point in points:
            if point[1] is None:
                with self.assertRaises(app_models.Region.DoesNotExist):
                    app_models.Region.get_for_point(point[0])
            else:
                self.assertEqual(
                    point[1], app_models.Region.get_for_point(point[0]).name
                )

        e1 = app_models.Encampment.objects.create(
            name="Test encampment",
            location="",
            location_geom=Point(-122.2245076, 37.7777988),
        )
        self.assertEqual(e1.region.name, "District 5")

        with self.assertRaises(app_models.Region.DoesNotExist):
            app_models.Encampment.objects.create(
                name="Test encampment",
                location="",
                location_geom=Point(-122.44994547, 37.76389937),
            )

    @freeze_time("2020-05-18")
    def test_visited_encampments(self):
        e1 = app_models.Encampment.objects.create(
            name="Test encampment",
            location="",
            location_geom=Point(-122.2245076, 37.7777988),
        )
        self.assertEqual(list(app_models.Encampment.not_visited_in(10)), [e1])

        app_models.Report.objects.create(
            encampment=e1,
            performed_by=self.org,
            date=date.today() - timedelta(days=3),
            talked_to=10,
            assessed=50,
            assessed_asymptomatic=12,
        )
        self.assertEqual(app_models.Encampment.not_visited_in(10).count(), 0)
        self.assertEqual(app_models.Encampment.not_visited_in(1).count(), 1)

    @freeze_time("2020-05-18")
    def test_next_visit(self):
        e1 = app_models.Encampment.objects.create(
            name="Test encampment",
            location="",
            location_geom=Point(-122.2245076, 37.7777988),
        )
        self.assertEqual(e1.next_visit(), None)
        self.assertEqual(e1.last_report(), None)

        scheduled_visit = ScheduledVisit.objects.create(
            encampment=e1, date=date.today()
        )
        self.assertEqual(e1.next_visit(), scheduled_visit)
        self.assertEqual(e1.last_report(), None)

        report = app_models.Report.objects.create(
            encampment=e1,
            performed_by=self.org,
            date=date.today(),
            visit=scheduled_visit,
            talked_to=10,
            assessed=50,
            assessed_asymptomatic=12,
        )

        self.assertEqual(e1.next_visit(), None)
        self.assertEqual(e1.last_report(), report)

    @freeze_time("2020-05-18")
    def test_tasks(self):
        e1 = app_models.Encampment.objects.create(
            name="Test encampment",
            location="",
            location_geom=Point(-122.2245076, 37.7777988),
        )
        self.assertEqual(e1.tasks.count(), 0)
        self.assertEqual(e1.open_tasks().count(), 0)

        task = app_models.Task.objects.create(
            title="Clean up trash",
            details="Trash everywhere, it's a mess",
            encampment=e1,
        )

        self.assertEqual(e1.tasks.count(), 1)
        self.assertEqual(e1.open_tasks().count(), 1)

        task.completed = timezone.now()
        task.save()

        self.assertEqual(e1.tasks.count(), 1)
        self.assertEqual(e1.open_tasks().count(), 0)
