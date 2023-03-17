from django.urls import path
from food import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registrated, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
    path('password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('lk/', views.detailprofile, name='lk'),
    path('card<int:pk>/', views.get_cards, name='card'),
    path('order/', views.order, name='order'),
    path('stub/', views.payment, name='stub'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
