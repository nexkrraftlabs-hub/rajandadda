from django import template
from home.models import Lead

register = template.Library()

@register.simple_tag
def unread_leads_count():
    return Lead.objects.filter(is_read=False).count()
