from django.contrib.gis import admin

from apps.access.models import InvitedEmail


class InvitedEmailAdmin(admin.ModelAdmin):
    pass


admin.site.register(InvitedEmail, InvitedEmailAdmin)
