from datetime import date
from datetime import datetime

import humanize
from django import template
from django.utils import timezone

register = template.Library()


def ago(value):
    if isinstance(value, datetime):
        delta = humanize.naturaldelta(timezone.now() - value)
    elif isinstance(value, date):
        delta = humanize.naturaldelta(date.today() - value)
    return f"{delta} ago"


register.filter("ago", ago)
