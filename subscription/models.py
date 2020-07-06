from django.db import models
from django.utils import timezone


class SubscribeModel(models.Model):
    email = models.EmailField('email', max_length=200, unique=True)
    status = models.CharField('status', max_length=64, blank=True)
    created_date = models.DateTimeField(
        'date', blank=True, auto_now_add=timezone.now)

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'

    def __str__(self):
        return self.email
