from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterUserForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


def index(request):
    return render(request, "index.html")


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')
