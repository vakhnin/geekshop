from django.contrib import auth, messages
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
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


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        form = UserRegisterForm()
    context = {
        'title': 'Geekshop - Регистрация',
        'form': form}
    return render(request, 'authapp/register.html', context)


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


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main')
