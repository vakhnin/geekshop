from django.contrib import auth, messages
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfilerForm
# Create your views here.
from authapp.models import ShopUser
from geekshop import settings
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
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.set_level(request, messages.SUCCESS)
                messages.success(request, 'Вы успешно зарегистрировались. '
                                          'На Ваш E-mail отправленно письмо, для подтверждения E-mail.')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.set_level(request, messages.ERROR)
                messages.error(request, form.errors)
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)
        context = {'form': form}
        return render(request, self.template_name, context)

    def send_verify_link(self, user):
        verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)


def verify(request, email, activate_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.is_active:
            messages.success(request, 'Электронная почта уже подтверждена.')
            return HttpResponseRedirect(reverse('authapp:login'))
        if user and user.activation_key == activate_key and not user.is_activation_key_expires():
            user.activation_key = ''
            user.activation_key_expires = None
            user.is_active = True
            user.save()

            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Электронная почта успешно подтверждена.')
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Не удалось подтвердить электронную почту. '
                                    'Обратитесь к администратору.')
        return HttpResponseRedirect(reverse('authapp:login'))
    except Exception as e:
        messages.set_level(request, messages.ERROR)
        messages.error(request, 'Не удалось подтвердить электронную почту. '
                                'Обратитесь к администратору.')
        return HttpResponseRedirect(reverse('authapp:login'))


class UserDetailView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    title = 'Geekshop - Регистрация'
    model = ShopUser
    form_class = UserProfilerForm
    success_url = reverse_lazy('authapp:profile')
    template_name = 'authapp/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Данные профиля успешно обновлены')
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors:
            messages.error(self.request, form.errors[error][0])
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main')
