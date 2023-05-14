from django.db import models
from django.utils.html import mark_safe
from datetime import datetime
# from PIL import Image

class Cities(models.Model):
    city_name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.id, self.city_name}'
        
class Categories(models.Model):
    category = models.CharField(max_length=16)
    fermentation = models.CharField(max_length=16)
    
    def __str__(self):
        return f'{self.category, self.fermentation}'

class Type_packaging(models.Model):
    # ассоциации
    LOOSE = 'Loose'
    СAKE = 'Сake'
    BOWL = 'Bowl'
    BRICK = 'Brick'
    SPHERE = 'Sphere'
    # список категорий (для выбора категории)
    CHOICE_GROUP = {
        (LOOSE, 'Loose'),
        (СAKE, 'Сake'),
        (BOWL, 'Bowl'),
        (BRICK, 'Brick'),
        (SPHERE,'Sphere'),
    }
    packaging = models.CharField(max_length=20, choices=CHOICE_GROUP, default=LOOSE)
    
    def __str__(self):
        return f'{self.packaging}'

class Teas(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.name}'

class Weight(models.Model):
    weight = models.IntegerField()
    def __str__(self):
        return f'{str(self.weight)}'


class Products(models.Model):
    tea = models.ForeignKey(Teas, on_delete = models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    packaging = models.ForeignKey(Type_packaging, on_delete=models.CASCADE)
    description = models.TextField()
    # weight = models.ForeignKey(Weight, on_delete=models.CASCADE)
    # amount =  models.IntegerField()
    # store = models.ForeignKey(Store, on_delete=models.CASCADE)
    # link = models.URLField(max_length=2000, null=True)
    image = models.ImageField(upload_to = 'tea/', null=True)
    
    def __str__(self):
        return "%s %s %s %s %s %s" % (
            'id: '+ str(self.id), self.tea, 
            self.category, self.description, 
            str(self.packaging), str(self.image),
        )


class Store(models.Model):
    # tea = models.ForeignKey(Teas, on_delete = models.CASCADE)
    product = models.ForeignKey(Products, on_delete = models.CASCADE)
    weight = models.ForeignKey(Weight, on_delete= models.CASCADE)
    amount = models.IntegerField()
    price = models.FloatField()
    
    def __str__(self):
        return f'{self.product, str(self.weight), str(self.amount), str(self.price)}'

class Users(models.Model):
    username = models.CharField(unique=True, max_length=25)
    email = models.EmailField(unique=True, max_length=64)
    password = models.CharField(max_length=64)
    user_city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.username, str(self.email)}'

class Cart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    date_order = models.DateTimeField(null=False)
    order_price = models.FloatField()

    def __str__(self):
        return f'{self.user, str(self.date_order), str(self.order_price)}'

class CartItems(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False)
    product_price = models.FloatField()

    def __str__(self):
        return f'{self.cart_id.date_order, self.cart_id.order_price, str(self.product), str(self.product_qty), str(self.product_price)}'