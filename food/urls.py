from django.urls import path
from food import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registrated, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login')
]
