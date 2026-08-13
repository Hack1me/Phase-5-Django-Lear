from django.urls import path

from .views import *

urlpatterns = [
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('dashboard/', dashboard, name='dashboard'),
    path('sign_out/', sign_out, name='sign_out'),
    path('', home, name='home'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset/done/', password_reset_done, name='password_reset_done'),
    path('password_reset/complete/', password_reset_complete, name='password_reset_complete'),
]