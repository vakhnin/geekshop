from django.views.generic import TemplateView
from products.mixin import AddTitleToContextMixin, UserIsSuperuserMixin


class IndexTemplateView(TemplateView, AddTitleToContextMixin, UserIsSuperuserMixin):
    template_name = 'admins/admin.html'
    title = 'Админка'
