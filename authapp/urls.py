from django.urls import path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.UserLoginView.as_view(), name='login'),
    path('logout/', authapp.UserLogoutView.as_view(), name='logout'),
    path('register/', authapp.UserRegisterView.as_view(), name='register'),
    path('profile/', authapp.UserDetailView.as_view(), name='profile'),

    path('verify/<str:email>/<str:activate_key>/', authapp.verify, name='verify'),
]
