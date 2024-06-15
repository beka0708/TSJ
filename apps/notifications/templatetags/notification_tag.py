from django import template
from apps.notifications.models import ToAdminNotification

register = template.Library()


@register.simple_tag
def get_notification():
    notification_list = ToAdminNotification.objects.filter(read=False)
    return notification_list


@register.simple_tag
def get_notification_count():
    notification_list = ToAdminNotification.objects.filter(read=False).count()
    return notification_list
