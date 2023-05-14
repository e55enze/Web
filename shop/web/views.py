# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, JsonResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from web.models import *
import re
import hashlib

# регистрация пользователя
def register(request):
    context = get_context(request)
    return render(request, 'web/register.html', context)

# создание нового пользователя
def create(request):
    response = HttpResponse("")
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            response = HttpResponse("Password mismatch")
        else:
            if len(password) >= 5:
                if any(ch.isdigit() for ch in password):
                    # check = lambda password: not all('a'<=x<='z' or 'A'<=x<='Z' for x in password)
                    regex = "[a-zA-Z]+$"
                    pattern = re.compile(regex)
                    print(pattern.search(password) is not None) # False
                    if re.search(pattern, password):
                        password_sha256 = hashlib.sha256(password.encode('UTF-8'))
                        password_hash = password_sha256.hexdigest()
                        print(password_hash)
                        # get instance city
                        city = Cities.objects.get(city_name="Moscow")
                        new_user = Users(username=username, email=email, password=password_hash, user_city=city)
                        new_user.save()
                        response = HttpResponse('New Profile Created Successfully!')
                    else:
                        response = HttpResponse("Password must contain at least 1 latin symbol!")
                else:
                    response = HttpResponse("Password must contain at least 1 digit!")
            else:
                response= HttpResponse("Password length must be at least 5 characters!")
    return response

# авторизация
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    print("username:", username, "\npassword:", password)
    users = Users.objects.all()
    flag_user = False
    flag = False
    response = HttpResponseRedirect("/")
    password_sha256 = hashlib.sha256(password.encode('UTF-8'))
    password_hash = password_sha256.hexdigest()
    for user in users:
        if user.username == username:
            flag_user = True
            password_sha256 = hashlib.sha256(password.encode('UTF-8'))
            password_hash = password_sha256.hexdigest()
            if password_hash == user.password:
                flag = True
            break
    if not flag_user:
        return HttpResponse("Error! \nUser with name: \"" + username + "\" not exist!")
    else:
        if flag:
            response.set_cookie("username", username)
            print('Set Cookie')
            return response
        else:
            return HttpResponse("Error! \nWrong password!")
    # return response

# деавторизация
def logout(request):
    # META - хранит все доступные заголовки http в виде словаря
    # HTTP_REFERER - страница, с которой клиент отправил запрос
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    response.delete_cookie('username')
    return response

# добавление товара в корзину
def add_to_cart(request):
    cart_p = {}
    cart_p[int(request.POST['id'])]={
        'title': request.POST['title'],
        'qty': int(request.POST['qty']),
        'price': request.POST['price'],
        'img': request.POST['image']
    }
    print(cart_p)
    if 'cartdata' in request.session:
        if request.POST['id'] in request.session['cartdata']:
            cart_data = request.session['cartdata']
            # cart_data[request.POST['id']]['qty'] += int(request.POST['qty'])
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    get_session(request)
    return JsonResponse({'data': cart_p})

# удаление товара из корзины в сессии
def delete_from_cart(request):
    product_id = int(request.GET['id'])
    print('delete product ', product_id , 'from cart')
    cart_d = {'id': request.GET['id']}
    cart_data = request.session['cartdata']
    del cart_data[request.GET['id']]
    cart_data.update()
    request.session['cartdata'] = cart_data     
    return JsonResponse({'data': cart_d})

# изменение корзины в сессии
def change_session(request):
    cart_p = {}
    cart_p[int(request.POST['id'])]={
        'qty': int(request.POST['qty']),
    }
    if 'cartdata' in request.session:
        if request.POST['id'] in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_temp = cart_data
            cart_data[request.POST['id']]['qty'] = int(request.POST['qty'])
            request.session['cartdata'] = cart_data   
    return JsonResponse({'data': cart_p})

# получение данных корзины из сессии
def get_session(request):
    cart_data = request.session['cartdata']
    if 'cartdata' in request.session:
        for key in cart_data:
            print('key: ', key, 'qty: ',cart_data[key]['qty'])
        return cart_data
    else:
        return False

# удаление сессии
def delete_session(request):
    try:
        del request.session['cartdata']
    except KeyError:
        print('Error! ',KeyError)
    return HttpResponse("<h1>Session Data cleared</h1>")

# домашняя страница сайта
def index(request):
    context = get_context(request)
    return render(request, 'web/index.html', context)

# профиль
def profile(request):
    context = get_context(request)
    if 'username' in request.COOKIES:
        user_name = request.COOKIES['username']  
        user = Users.objects.all().values()
        user = user.filter(username=user_name).values()
        print(user[0])
        context['user_info'] = user[0]
    return render(request, 'web/profile.html', context)

# корзина
def cart(request):
    context = get_context(request)
    products = Products.objects.all()
    cartdata= context.get('cartdata')
    print('\ncartdata: ',cartdata)
    cart_id = list(cartdata.keys())
    products = products.filter(pk__in=cart_id)
    context['products'] = products
    return render(request, 'web/cart.html', context)

# оформление заказа
def checkout(request):
    # final order price
    order_price = request.GET['order_price']
    # date & time order (UTC)
    dateTime = datetime.utcnow()
    user_name = request.COOKIES['username']  
    user = Users.objects.all().values()
    user = user.filter(username=user_name).values()
    user_id = user[0].get('id')
    # get user instance
    user_id = Users.objects.get(id=user_id)
    cart = Cart(user=user_id, date_order=dateTime, order_price=float(order_price))
    cart.save()
    cart_data = {}
    if 'cartdata' in request.session:
        cart_data = request.session['cartdata']
    # key - id, value - [title, qty, price, img]
    for key, value in cart_data.items():
        product = Products.objects.get(id=key)
        qty = value['qty']
        price = float(value['price'])
        cartItem = CartItems(cart_id=cart, product=product, product_qty=qty, product_price=price)
        cartItem.save()
    # clear session
    cart_data = {}
    if 'cartdata' in request.session:
        request.session['cartdata'] = cart_data
    return JsonResponse({'order_price': order_price})

# товары
def products(request):
    context = get_context(request)
    return render(request, 'web/products.html', context)

# Сортировка
def sorting(request):
    context = get_context(request)
    print(request)
    products = []
    if str(request).__contains__('sort-amount-up'):
        store = Store.objects.all().order_by('amount').values()
        for value in store:
            # print(value['id'])
            product = Products.objects.get(id=value['id'])
            products.append(product)

    if str(request).__contains__('sort-amount-down'):
        store = Store.objects.all().order_by('-amount').values()
        for value in store:
            product = Products.objects.get(id=value['id'])
            products.append(product)

    if str(request).__contains__('sort-price-up'):
        store = Store.objects.all().order_by('price').values()
        for value in store:
            product = Products.objects.get(id=value['id'])
            products.append(product)

    if str(request).__contains__('sort-price-down'):
        store = Store.objects.all().order_by('-price').values()
        for value in store:
            product = Products.objects.get(id=value['id'])
            products.append(product)

    context['products'] = products
    return render(request, 'web/products.html', context)

# Фильтрация
def filtering(request):
    context = get_context(request)
    filter_cat = ''
    if str(request).__contains__('filter-white'):
        filter_cat = 'White'
    if str(request).__contains__('filter-green'):
        filter_cat = 'Green'
    if str(request).__contains__('filter-oolong'):
        filter_cat = 'Oolong'
    if str(request).__contains__('filter-red'):
        filter_cat = 'Red'
    if str(request).__contains__('filter-puerh'):
        filter_cat = 'Pu-erh'
    category = Categories.objects.get(category=filter_cat)
    products = Products.objects.filter(category=category)
    context['products'] = products
    return render(request, 'web/products.html', context)

# Отзывы
def reviews(request):
    return render(request, 'web/reviews.html')

# контекст - данные из моделей, которые будут
# использоваться в шаблоне
def get_context(request):
    city = Cities.objects.all()
    products = Products.objects.all()
    stores = Store.objects.all()
    cart_data = {}
    context = {
        'products': products,
        'stores': stores,
        'city': city,
        'cartdata': cart_data
    }
    # получение города юзера из куков
    if 'user_city' in request.COOKIES:
        user_city = request.COOKIES['user_city']
        context['user_city'] = user_city
    username = ''
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
        context['username'] = username
        if 'cartdata' in request.session:
            cart_data = request.session['cartdata']
        else:
            request.session['cartdata'] = cart_data
    return context

# Добавление города в куки
def set_city(request):
    city = request.GET.get("city", "Undefined")
    response = HttpResponsePermanentRedirect("/")
    # занесение куки user_city со значением города
    response.set_cookie('user_city', city)
    return response