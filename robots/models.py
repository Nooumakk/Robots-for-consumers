from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from R4C.task import send_email


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=True, null=True)
    model = models.CharField(max_length=2)
    version = models.CharField(max_length=2)
    created = models.DateTimeField()


@receiver(pre_save, sender=Robot)
def robot_pre_save(sender, instance: Robot, **kwargs):
    instance.model = instance.model.upper()
    instance.version = instance.version.upper()
    instance.serial = f"{instance.model}-{instance.version}"


@receiver(post_save, sender=Robot)
def order_post_save(sender, instance: Robot, **kwargs):
    from orders.models import Order

    orders = Order.objects.filter(robot_serial=instance.serial, is_active=True)
    for order in orders:
        subject = f"Заказ для робота {order.robot_serial}"
        message = f"Добрый день!\nНедавно вы интересовались нашим роботом модели {instance.model}, версии {instance.serial}. Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
        recipient_list = order.customer.email

        send_email.delay(subject, message, recipient_list)
        order = Order.objects.get(pk=order.id)
        order.is_active = False
        order.save()
