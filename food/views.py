from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import RegisterUserForm, UserProfileForm
from django.views.generic import UpdateView


def index(request):
    return render(request, "index.html")


def registrated(request):
    form = {}

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует!')
        else:
            if form.is_valid():
                ins = form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']

                user = authenticate(username=username, password=password, email=email)
                ins.email = email
                ins.save()
                form.save_m2m()
                return redirect('index')
    else:
        form = RegisterUserForm(request.POST)
    return render(request, 'registration.html', context={'form': form})


def order(request):
    return render(request, "order.html")


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
    return render(request, 'lk.html', {'form': form})
