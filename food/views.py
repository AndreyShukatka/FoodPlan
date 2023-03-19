import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Order, Menu, Category, Subscription, Recipe
from .forms import RegisterUserForm, UserProfileForm, UserPasswordChangeForm

from dateutil.relativedelta import relativedelta


def index(request):
    free_dishes = Recipe.objects.filter(free=True)
    data = {'free_dishes':free_dishes}
    return render(request, "index.html", context=data)



def registrated(request):
    form = {}

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password1')
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
                user = authenticate(username=username, password=password)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('index')
    else:
        form = RegisterUserForm(request.POST)
    return render(request, 'registration.html', context={'form': form})


def order(request):
    if request.user.user_orders.check_active_order == True:
        return redirect('all_card')
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
        return redirect('order_payment', pk=order.pk)

    menu_types = Menu.objects.all()
    subscriptions = Subscription.objects.all()
    return render(request, "order.html", context={
        'menu_types': menu_types,
        'categories': categories,
        'subscriptions': subscriptions
    })


def order_payment(request, pk):
    try:
        order = Order.objects.get(id=pk)
        if order.user != request.user:
            order = {}
    except:
        order = {}
    return render(request, "order_payment.html", {'order': order,})

def success_payment(request, pk):
    try:
        order = Order.objects.get(id=pk)
        if order.paid:
            return render(request, "success_payment.html", {})
        order.paid = True
        order.payment_date = datetime.datetime.now()
        order.save()
        order.last_day_order = order.payment_date + relativedelta(months=int(order.subscription.period))
        return render(request, "success_payment.html", {'order': order,})
    except:
        return render(request, "success_payment.html", {})


def get_card(request, pk):
    recipe = Recipe.objects.get(id=pk)
    return render(request, "card2.html", {'recipe': recipe})


def get_all_cards(request):
    if request.user.user_orders.check_active_order == True:
        return redirect('all_card')
    user_order = request.user.user_orders.active_order()
    days = {}
    for day in range(1,8):
        days[day] = {
            'number': day,
            'categories': []
        }
        for category in user_order.category.all():
            if Recipe.objects.filter(category=category):
                recipe = Recipe.objects.filter(
                    menu=user_order.menu_type,
                    category=category
                ).order_by('?')[0]
            else:
                continue
            days[day]['categories'].append(recipe)
    recipes = Recipe.objects.filter(
        menu=user_order.menu_type,
        category__in=user_order.category.all()
    )
    return render(request, "all_cards.html", {'recipes': recipes, 'days': days})


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

