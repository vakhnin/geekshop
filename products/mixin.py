from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.base import View, ContextMixin


class UserIsSuperuserMixin(View):

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserIsSuperuserMixin, self).dispatch(request, *args, **kwargs)


class AddTitleAndNavActiveToContextMixin(ContextMixin):
    title = ''
    nav_active = ''

    def get_context_data(self, **kwargs):
        context = super(AddTitleAndNavActiveToContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['nav_active'] = self.nav_active
        return context
