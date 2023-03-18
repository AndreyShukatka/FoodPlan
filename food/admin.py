from django.contrib import admin
from .models import Subscription, Menu, Category, Order, Recipe, Ingredient


admin.site.register(Subscription)
admin.site.register(Menu)
admin.site.register(Category)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'paid',
        'payment_date',
        'menu_type',
        'subscription',
        'person_count',
    ]

admin.site.register(Recipe)
admin.site.register(Ingredient)
