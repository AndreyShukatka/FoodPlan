from django.urls import path
from food import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registrated, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
    path('lk/', views.detailprofile, name='lk'),
    path('order/', views.order, name='order'),
    path('payment/', views.payment, name='payment'),
]
