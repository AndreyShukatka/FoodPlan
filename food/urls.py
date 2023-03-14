from django.urls import path
from food import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.RegisterUser.as_view(), name='registration')
]
