from django.contrib.gis import admin

from apps.reporting.models import Encampment
from apps.reporting.models import Region


class EncampmentAdmin(admin.OSMGeoAdmin):
    readonly_fields = ("region",)
    modifiable = False


admin.site.register(Encampment, EncampmentAdmin)


class RegionAdmin(admin.OSMGeoAdmin):
    modifiable = False


admin.site.register(Region, RegionAdmin)
