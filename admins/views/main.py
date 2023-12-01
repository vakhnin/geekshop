from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from products.mixin import AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin


class IndexTemplateView(TemplateView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    template_name = 'admins/admin.html'
    title = 'Админка'
