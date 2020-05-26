from datetime import date

import humanize
from django import template

register = template.Library()


def ago(value):
    delta = humanize.naturaldelta(date.today() - value)
    return f"{delta} ago"


register.filter("ago", ago)
