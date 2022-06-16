from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.base import View, ContextMixin


class UserIsSuperuserMixin(View):

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserIsSuperuserMixin, self).dispatch(request, *args, **kwargs)


class AddTitleToContextMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        context = super(AddTitleToContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class UserIsLoginMixin(View):

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        return super(UserIsLoginMixin, self).dispatch(request, *args, **kwargs)
