from django.contrib.gis import admin

from apps.reporting.models import Encampment
from apps.reporting.models import Organization
from apps.reporting.models import Region


class EncampmentAdmin(admin.OSMGeoAdmin):
    readonly_fields = ("region",)
    modifiable = False


class RegionAdmin(admin.OSMGeoAdmin):
    modifiable = False


class OrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Encampment, EncampmentAdmin)
admin.site.register(Region, RegionAdmin)
