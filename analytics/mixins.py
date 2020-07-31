from analytics.signals import object_viewed_signal


class ObjectViewMixin(object):
    def get_context_data(self, *args, **kwargs):
        instance = kwargs.get('object')
        if instance:
            object_viewed_signal.send(
                instance.__class__,
                instance=instance,
                request=self.request)

        return super().get_context_data(*args, **kwargs)
