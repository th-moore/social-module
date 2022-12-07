from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    notification_event_digest = models.BooleanField(default=False)
    notification_group_digest = models.BooleanField(default=False)
    notification_post_replies = models.BooleanField(default=False)