from django.contrib.sites.models import Site


def current_site(request):
    """
    A context processor to add the "current site" to the current Context
    """
    try:
        current_site = Site.objects.get_current()
        return {
            "current_site": current_site,
        }
    except Site.DoesNotExist:
        return {"current_site": "Encampment Tracker"}
