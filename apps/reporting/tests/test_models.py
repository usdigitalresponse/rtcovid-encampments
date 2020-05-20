from django.contrib.gis.geos import Point
from django.core.management import call_command
from django.test import TestCase

from apps.reporting import models as app_models


class TestModels(TestCase):
    def setUp(self):
        call_command("preload_oakland")

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
            e2 = app_models.Encampment.objects.create(
                name="Test encampment",
                location="",
                location_geom=Point(-122.44994547, 37.76389937),
            )
