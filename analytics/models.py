from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.sessions.models import Session
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from analytics.utils import get_client_ip
from accounts.signals import user_logged_in
from analytics.signals import object_viewed_signal

from shop.models import CategoryModel

User = get_user_model()

FORCE_SESSION_TO_ONE = getattr(
    settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(
    settings, 'FORCE_INACTIVE_USER_ENDSESSION', False)


class ObjectViewedQuerySet(models.query.QuerySet):
    def by_model(self, model_class, model_queryset=False):
        content_type = ContentType.objects.get_for_model(model_class)
        queryset = self.filter(content_type=content_type)

        if model_queryset:
            ids = [qs.object_id for qs in queryset]
            return model_class.objects.filter(pk__in=ids)
        return queryset


class ObjectViewedManager(models.Manager):
    def get_queryset(self):
        return ObjectViewedQuerySet(self.model, using=self._db)

    def by_model(self, model_class, model_queryset=False):
        return self.get_queryset().by_model(
            model_class, model_queryset=model_queryset)


class ObjectViewedModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    ip_address = models.CharField(max_length=225, blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True)

    objects = ObjectViewedManager()

    def __str__(self):
        return "{} viewed on {}".format(
            self.content_object, self.created)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Product viewed'
        verbose_name_plural = 'Products viewed'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    content_type = ContentType.objects.get_for_model(sender)
    user = None
    try:
        if request.user.is_authenticated or None:
            user = request.user
    except:
        pass

    ObjectViewedModel.objects.get_or_create(
        user=user, content_type=content_type,
        object_id=instance.id,
        ip_address=get_client_ip(request))

object_viewed_signal.connect(object_viewed_receiver)


class UserSessionModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    ip_address = models.CharField(max_length=225, blank=True, null=True)
    session_key = models.CharField(max_length=225, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_ended = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        try:
            Session.objects.get(pk=session_key).delete()
            self.is_active = False
            self.is_ended = True
            self.save()
        except:
            pass
        return self.is_ended


def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSessionModel.objects.filter(
            user=instance.user, is_ended=False,
            active=False).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()
if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSessionModel)


def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active is False:
            qs = UserSessionModel.objects.filter(
                user=instance.user, is_ended=False,
                is_active=False)
            for i in qs:
                i.end_session()

if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changed_receiver, sender=User)


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSessionModel.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key)

user_logged_in.connect(user_logged_in_receiver)


class CategoryViewManager(models.Manager):
    def add_count(self, user, category):
        category, created = self.model.objects.get_or_create(
            user=user, category=category)
        category.count += 1
        category.save()
        return category


class CategoryView(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True)
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.SET_NULL,
        blank=True, null=True)
    count = models.IntegerField(default=0)

    objects = CategoryViewManager()

    def __str__(self):
        return self.category.name
