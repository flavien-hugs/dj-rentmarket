from django.http import Http404
from django.utils.http import is_safe_url
from django.utils.decorators import method_decorator


def ajax_required(function):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


class AjaxRequiredMixin(object):
    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class NextUrlMixin(object):
    default_next = "home"

    def get_next_url(self):
        next_ = self.request.GET.get('next')
        next_post = self.request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path, self.request.get_host()):
                return redirect_path
        return self.default_next
