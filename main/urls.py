from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page),
    path('user/register_page', views.register_page),
    path('user/register', views.register),
    path('user/login_page', views.login_page),
    path('user/login', views.login),
    path('user/account_page', views.account_page),
    path('user/update_info', views.update_info),
    path('user/logout', views.logout),
]