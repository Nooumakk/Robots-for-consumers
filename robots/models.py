from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=True, null=True)
    model = models.CharField(max_length=2)
    version = models.CharField(max_length=2)
    created = models.DateTimeField()


@receiver(pre_save, sender=Robot)
def robot_pre_save(sender, instance: Robot, **kwargs):
    created_datetime = datetime.strptime(str(instance.created), "%Y-%m-%d %H:%M:%S")
    instance.created = timezone.make_aware(created_datetime, timezone=timezone.get_current_timezone())
    instance.serial = f"{instance.model}-{instance.version}"
