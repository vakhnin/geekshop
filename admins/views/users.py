from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm
from authapp.models import ShopUser
from products.mixin import AddTitleAndNavActiveToContextMixin


# Create your views here.
class UserCreateView(CreateView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = ShopUser
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Создать пользователя'

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'

    no_permission_template_name = 'admins/admin-no-permission.html'

    def get_template_names(self):
        if self.request.user.is_staff:
            return super().get_template_names()
        else:
            return self.no_permission_template_name


class UserListView(ListView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = ShopUser
    template_name = 'admins/admin-users-read.html'
    title = 'Админка | Пользователи'

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'

    no_permission_template_name = 'admins/admin-no-permission.html'

    def get_template_names(self):
        if self.request.user.is_staff:
            return super().get_template_names()
        else:
            return self.no_permission_template_name


class UserUpdateView(UpdateView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = ShopUser
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    title = 'Админка | Обновление пользователя'

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'

    no_permission_template_name = 'admins/admin-no-permission.html'

    def get_template_names(self):
        if self.request.user.is_staff:
            return super().get_template_names()
        else:
            return self.no_permission_template_name

    def post(self, request, *args, **kwargs):
        user = ShopUser.objects.get(id=kwargs['pk'])
        form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=user)
        if not form.is_valid():
            for error_field in form.errors:
                for error_message in form.errors[error_field]:
                    messages.error(self.request, error_message)
        else:
            messages.success(self.request, 'Данные профиля успешно обновлены')
            form.save()
        return redirect(reverse_lazy('admins:admin_users_update', kwargs={'pk': self.kwargs['pk']}))


class UserDeleteView(DeleteView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = ShopUser
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Удалить пользователя'

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'

    no_permission_template_name = 'admins/admin-no-permission.html'

    def get_template_names(self):
        if self.request.user.is_staff:
            return super().get_template_names()
        else:
            return self.no_permission_template_name

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
