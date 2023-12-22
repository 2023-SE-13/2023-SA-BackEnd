from django.utils import timezone
import datetime


def get_expiry_time():
    return timezone.now() + datetime.timedelta(minutes=10)
