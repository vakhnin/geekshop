from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm
from authapp.models import ShopUser
from products.mixin import AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin


# Create your views here.
class UserCreateView(CreateView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = ShopUser
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Создать пользователя'


class UserListView(ListView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = ShopUser
    template_name = 'admins/admin-users-read.html'
    title = 'Админка | Пользователи'


class UserUpdateView(UpdateView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = ShopUser
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Обновление пользователя'


class UserDeleteView(DeleteView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = ShopUser
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Удалить пользователя'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
