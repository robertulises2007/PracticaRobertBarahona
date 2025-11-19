from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def time_ago(value):
    if not value:
        return ""
    now = timezone.now()
    diff = now - value
    if diff < timedelta(minutes=1):
        return "Hace unos segundos"
    elif diff < timedelta(hours=1):
        return f"{int(diff.total_seconds() // 60)}m"
    elif diff < timedelta(hours=24):
        return f"{int(diff.total_seconds() // 3600)}h"
    elif diff < timedelta(days=2):
        return "Ayer"
    else:
        return value.strftime("%d/%m/%Y %I:%M %p")
