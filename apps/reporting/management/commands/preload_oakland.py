import json

import requests
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiPolygon
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from apps.reporting.models import Region


OAK_COUNCILS_DATA_URL = (
    "http://data.openoakland.org/sites/default/files/OakCCD2013.json"
)


class Command(BaseCommand):
    help = "Loads various Oakland-specific data, like city council districts."

    def load_council_districts(self):
        self.stdout.write(" - Importing Oakland City Council districts...")
        count = 0
        data = requests.get(url=OAK_COUNCILS_DATA_URL).json()

        for feature in data["features"]:
            geom = GEOSGeometry(str(feature["geometry"]))

            # Make sure all are MultiPolygons
            if geom.geom_type == "Polygon":
                geom = MultiPolygon(geom)

            # Munge the name into something sensible
            name = "District {}".format(feature["properties"]["Name"])

            r, created = Region.objects.get_or_create(name=name, geom=geom,)
            if created:
                count += 1
        self.stdout.write(
            self.style.SUCCESS("    -> Loaded {} districts.".format(count))
        )

    def handle(self, *args, **options):
        self.stdout.write("Beginning Oakland preloads...")
        self.load_council_districts()
        self.stdout.write(self.style.SUCCESS("Finished Oakland preloads."))
