import random
import requests
import string
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiPolygon
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection

from apps.reporting import models as reporting_models

PREREQUISITE_COMMANDS = {
    "oakland": ["preload_oakland",],
}

ordinal = lambda n: "%d%s" % (
    n,
    {1: "st", 2: "nd", 3: "rd"}.get(n if n < 20 else n % 10, "th"),
)


class Command(BaseCommand):
    help = "Bootstrap a dev environment for a particular city"

    def add_arguments(self, parser):
        parser.add_argument("city", nargs=1, type=str)

    def letter_from_int(self, num):
        num_alpha = dict(zip(range(1, 27), string.ascii_lowercase))
        result = ""
        loop_count = (num - 1) // 26

        if loop_count > 0:
            result = result + self.letter_from_int(loop_count)

        remainder = num % 26
        if remainder > 0:
            return result + num_alpha[remainder]
        return result + "z"

    def make_random_location(self, count):
        # Trying to be fun, I guess
        suffices = ["Ave", "St", "Blvd", "Rd", "Rt"]
        if count % 2:
            result = "{} {} {}.".format(
                random.randrange(1, 99999),
                ordinal(count),
                suffices[count % len(suffices)],
            )
        else:
            st1 = "{} {}.".format(
                self.letter_from_int(count).upper(), random.choice(suffices)
            )
            st2 = "{} {}.".format(ordinal(count), random.choice(suffices))
            result = "{} at {}".format(st1, st2)
        self.stdout.write(self.style.HTTP_INFO("Created encampment: {}".format(result)))
        return result

    def make_random_encampments(self):
        count = 0
        for r in reporting_models.Region.objects.all():
            sql = "SELECT ST_AsEWKT(ST_GeneratePoints(ST_GeomFromEWKT('{ewkt}'), 4))"
            cursor = connection.cursor()
            cursor.execute(sql.format(ewkt=r.geom.wkt))
            points = GEOSGeometry(cursor.fetchall()[0][0])

            for point in points:
                reporting_models.Encampment.objects.create(
                    name="Encampment {}".format(count),
                    location=self.make_random_location(count),
                    location_geom=point,
                )
                count += 1

    def run_prerequisites(self, city):
        commands = PREREQUISITE_COMMANDS[city.lower()]
        for command in commands:
            call_command(command)

    def handle(self, *args, **options):
        city = options["city"][0]
        self.stdout.write("Bootstrapping for {}".format(city))
        self.run_prerequisites(city)
        self.make_random_encampments()
        self.stdout.write(self.style.SUCCESS("Finished {} preloads.".format(city)))
