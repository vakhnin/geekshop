from django.views.generic import TemplateView
from products.mixin import AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin


class IndexTemplateView(TemplateView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    template_name = 'admins/admin.html'
    title = 'Админка'
