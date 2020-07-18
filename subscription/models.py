from django.db import models
from django.utils import timezone


class SubscribeModel(models.Model):
    email = models.EmailField('email', max_length=200, unique=True)
    name = models.CharField('Nom', max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(
        auto_now_add=timezone.now, auto_now=False)
    created = models.DateTimeField(
        'date', auto_now=timezone.now, auto_now_add=False)

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'

    def __str__(self):
        return self.email
