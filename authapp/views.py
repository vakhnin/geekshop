from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfilerForm
# Create your views here.
from authapp.models import ShopUser
from baskets.models import Basket
from products.mixin import BaseClassContextMixin


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


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfilerForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные профиля успешно обновленны')
        else:
            for error in form.errors:
                messages.error(request, form.errors[error][0])

    context = {
        'title': 'Geekshop | Профайл',
        'form': UserProfilerForm(instance=request.user),
        'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'authapp/profile.html', context)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main')
