from django.contrib import admin
from .models import Subscription, Menu, Category, Order, Recipe


admin.site.register(Subscription)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Recipe)
