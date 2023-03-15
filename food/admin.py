from django.contrib import admin
from .models import Subscription, Menu, Category, Order, Recipe, Ingredient


admin.site.register(Subscription)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Recipe)
admin.site.register(Ingredient)
