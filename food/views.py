from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Order, Menu, Category, Subscription
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import RegisterUserForm, UserProfileForm, UserPasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
import datetime
from django.db import transaction


def index(request):
    return render(request, "index.html")


def registrated(request):
    form = {}

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        print(form.field_order)
        form.fields['first_name'] = form.fields['username']
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует!')
        else:
            if form.is_valid():
                ins = form.save()
                ins.email = email
                ins.first_name = first_name
                ins.save()
                form.save_m2m()
                return redirect('index')
    else:
        form = RegisterUserForm(request.POST)
    return render(request, 'registration.html', context={'form': form})


def order(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            menu_type=Menu.objects.get(pk=request.POST.get('foodtype')),
            subscription=Subscription.objects.get(pk=request.POST.get('subscription')),
            person_count=request.POST.get('person_count')
        )
        for category in categories:
            if request.POST.get(f'category_{category.pk}') == '0':
                order.category.add(category)
        return redirect('stub')

    menu_types = Menu.objects.all()
    subscriptions = Subscription.objects.all()
    return render(request, "order.html", context={
        'menu_types': menu_types,
        'categories': categories,
        'subscriptions': subscriptions
    })


def card(request):
    card = request.path.strip('/')
    return render(request, f"{card}.html")


def payment(request):
    return render(request, 'stub.html')


def detailprofile(request):
    users = User.objects.all()
    if request.method == 'POST':
        email = request.POST.get('email')
        if users.filter(email=email) and not users.filter(id=request.user.id, email=email):
            form = UserProfileForm(instance=request.user)
            return render(request, 'lk.html', {'form': form, 'error_email': 'Такой email уже существует!'})
        form = UserProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('lk')
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'lk.html', {'form': form, 'details': get_detail_order(request)})

def get_detail_order(request):
    try:
        order = Order.objects.get(user=request.user)
        subscription_period = order.subscription.get_period_display
        subscription_price = order.subscription.price
        paid = order.paid
        payment_date = order.payment_date
        end_date = payment_date + datetime.timedelta(days=30 * int(order.subscription.period))
        menu_type = order.menu_type
        category = order.category ## Может быть несколько
        person_count = order.person_count
        detail_order = {
            'subscription_period': subscription_period,
            'subscription_price': subscription_price,
            'paid': paid,
            'payment_date': payment_date,
            'end_date' : end_date,
            'menu_type': menu_type,
            'category': category,
            'person_count': person_count,
        }
    except Order.DoesNotExist:
        detail_order = None
    return detail_order

class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    """
    Изменение пароля пользователя
    """
    form_class = UserPasswordChangeForm
    template_name = 'change_password.html'
    success_message = 'Ваш пароль был успешно изменён!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пароля на сайте'
        return context

    def get_success_url(self):
        return reverse_lazy('lk')
