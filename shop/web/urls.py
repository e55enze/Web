from django.urls import path, re_path, include
from . import views

sortpatterns = [
    path("sort-amount-up/", views.sorting, name='sort-amount-up'),
    path("sort-amount-down/", views.sorting, name='sort-amount-down'),
    path("sort-price-up/", views.sorting, name='sort-price-up'),
    path("sort-price-down/", views.sorting, name='sort-price-down'),
    path("filter-white/", views.filtering, name='filter-white'),
    path("filter-green/", views.filtering, name='filter-green'),
    path("filter-oolong/", views.filtering, name='filter-oolong'),
    path("filter-red/", views.filtering, name='filter-red'),
    path("filter-puerh/", views.filtering, name='filter-puerh'),
]

urlpatterns = [
    re_path(r"^delete-from-cart/", views.delete_from_cart),
    re_path(r"^change-session/", views.change_session),
    re_path(r"set-city/", views.set_city),
    re_path(r"logout/", views.logout, name ='logout'),
    re_path(r"register/", views.register, name='register'),
    re_path(r"create/", views.create, name='create'),
    re_path(r"^delete-from-cart/", views.delete_from_cart),
    re_path(r"^change-session/", views.change_session),
    re_path(r"^cart/checkout/", views.checkout),
    path('', views.index, name='home'),
    path("products/", include(sortpatterns)),
    path('products/', views.products, name='products'),
    path('login/', views.login, name='login'),
    path('reviews/', views.reviews, name='reviews'),
    path('add-to-cart/', views.add_to_cart),
    path('add_data_db/',views.add_data_db),
    path('cart/',views.cart, name='cart'),
    path('profile/', views.profile, name='profile'),
    path('delete-session/',views.delete_session),
]