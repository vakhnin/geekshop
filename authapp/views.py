from django.contrib import auth, messages
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfilerForm
# Create your views here.
from authapp.models import ShopUser
from baskets.models import Basket
from products.mixin import BaseClassContextMixin, UserDispatchMixin


class UserLoginView(FormView, BaseClassContextMixin):
    model = ShopUser
    form_class = UserLoginForm
    success_url = reverse_lazy('main')
    template_name = 'authapp/login.html'
    title = 'Geekshop - Авторизация'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request, user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UserRegisterView(FormView):
    model = ShopUser
    form_class = UserRegisterForm
    success_url = reverse_lazy('authapp:login')
    template_name = 'authapp/register.html'
    title = 'Geekshop - Регистрация'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            print(2222)
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UserDetailView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    title = 'Geekshop - Регистрация'
    model = ShopUser
    form_class = UserProfilerForm
    success_url = reverse_lazy('authapp:profile')
    template_name = 'authapp/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Данные профиля успешно обновлены')
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors:
            messages.error(self.request, form.errors[error][0])
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main')
