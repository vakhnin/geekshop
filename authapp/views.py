from django.contrib import auth, messages
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
# Create your views here.
from authapp.models import ShopUser
from baskets.models import Basket
from geekshop import settings
from products.mixin import AddTitleAndNavActiveToContextMixin, UserIsLoginMixin


class UserLoginView(FormView, AddTitleAndNavActiveToContextMixin):
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
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def user_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        baskets = Basket.objects.filter(user=user)
        context = {
            'user_is_authenticated': user is not None,
            'user': user,
            'baskets': baskets}
        content = render_to_string('products/includes/navbar.html', context)

        error = ''
        if user is None:
            error = 'Неверные логин или пароль'

        return JsonResponse({'error': error,
                             'content': content})


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


def key_not_in_dict_or_empty_value(dict_, key):
    if key not in list(dict_.keys()):
        return True
    elif not dict_[key]:
        return True
    else:
        return False


def user_register_view(request):
    if request.method == "POST":
        error = ''
        user = None
        post_dict = request.POST.dict()

        if key_not_in_dict_or_empty_value(post_dict, 'username'):
            error = 'Поле "Имя пользователя" должно быть заполнено.'
        elif ShopUser.objects.filter(username=post_dict['username']):
            error = 'Пользователь с таким логином уже существует.'
        elif key_not_in_dict_or_empty_value(post_dict, 'email'):
            error = 'Поле "Адрес электронной почты" должно быть заполнено.'
        elif ShopUser.objects.filter(email=post_dict['email']):
            error = 'Пользователь с таким адресом электронной почты уже существует.'
        elif key_not_in_dict_or_empty_value(post_dict, 'password1'):
            error = 'Поле "Пароль" должно быть заполнено.'
        elif key_not_in_dict_or_empty_value(post_dict, 'password2'):
            error = 'Поле "Подтверждение пароля" должно быть заполнено.'
        elif post_dict['password1'] != post_dict['password2']:
            error = '"Пароль" и "Подтверждение пароля" не совпадают.'
        else:
            try:
                post_dict['password'] = post_dict['password1']
                del (post_dict['password1'])
                del (post_dict['password2'])
                user = ShopUser.objects.create_user(**post_dict)
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            except (ValueError, TypeError, KeyError) as e:
                error = 'Неизвестная ошибка. Обратитесь к разработчику.'
                print(e)

        context = {
            'user_is_authenticated': user is not None,
            'user': user,
            'baskets': None}
        content = render_to_string('products/includes/navbar.html', context)
        return JsonResponse({'error': error,
                             'content': content})


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


class UserDetailView(UpdateView, AddTitleAndNavActiveToContextMixin, UserIsLoginMixin):
    title = 'Geekshop - Профиль'
    nav_active = 'user'
    model = ShopUser
    form_class = UserProfileForm
    success_url = reverse_lazy('authapp:profile')
    template_name = 'authapp/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=request.user.userprofile)
        if not form.is_valid():
            messages.error(self.request, form.errors)
        elif not profile_form.is_valid():
            messages.error(self.request, profile_form.errors)
        else:
            messages.success(self.request, 'Данные профиля успешно обновлены')
            form.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data()
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main')
