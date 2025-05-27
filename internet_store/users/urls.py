from django.urls import path, include
from. import views

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('account/<int:user_id>', views.account, name='account')
]