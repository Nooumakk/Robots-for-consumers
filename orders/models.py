from django.db import models

from customers.models import Customer

from django.db.models.signals import  pre_save
from django.dispatch import receiver
from R4C.task import send_email


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)
    is_active = models.BooleanField(default=True)


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance: Order, **kwargs):
    from robots.models import Robot

    instance.robot_serial = instance.robot_serial.upper()
    robot = Robot.objects.filter(serial=instance.robot_serial).first()
    if robot:
        subject = f"Заказ для робота {instance.robot_serial}"
        message = f"Добрый день!\nНедавно вы интересовались нашим роботом модели {robot.model}, версии {robot.version}. Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
        recipient_list = instance.customer.email

        send_email.delay(subject, message, recipient_list)
        instance.is_active = False
