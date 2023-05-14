from django.contrib import admin
from .models import *
from django.apps import apps
from django.http import HttpResponse
from django.urls import path

# admin.site.register(Cities)

@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ('id','city_name')

@admin.register(Teas)
class TeasAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category', 'fermentation')

@admin.register(Type_packaging)
class Type_packagingAdmin(admin.ModelAdmin):
    list_display = ('packaging',)

@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ('weight',)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('tea', 'category', 'description', 'packaging', 'image')

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('product', 'weight', 'amount', 'price')

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'user_city')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_order', 'order_price')

@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'product', 'product_qty', 'product_price')
