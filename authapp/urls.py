from django.urls import path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    # path('login/', authapp.UserLoginView.as_view(), name='login'),
    # path('register/', authapp.UserRegisterView.as_view(), name='register'),
    path('login/', authapp.user_login_view, name='login'),
    path('logout/', authapp.UserLogoutView.as_view(), name='logout'),
    path('register/', authapp.user_register_view, name='register'),
    path('profile/', authapp.UserDetailView.as_view(), name='profile'),
    path('change-password/', authapp.change_password, name='change-password'),

    path('login-required/', authapp.UserLoginRequired.as_view(), name='login-required'),

    path('verify/<str:email>/<str:activate_key>/', authapp.verify, name='verify'),
]
