from django.test import TestCase
from http.cookies import SimpleCookie
from web.models import *

print("Unit-Testing: \n ")
class TestViews(TestCase):
    
    def test_index(self):
        print("url / ")
        response = self.client.get('')
        # проверка соответствия статус коду при обращении
        # к конкретной странице
        self.assertEqual(response.status_code, 200)

    def test_products(self):
        print("url /products")
        response =self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        # проверка наличия подстроки в содержимом страницы
        self.assertIn('By category', response.content.decode())
        self.assertIn('By quantity', response.content.decode())
        self.assertIn('By price', response.content.decode())

    def test_city(self):
        print("url /set-city")
        response =self.client.get('/set-city/', {'city': 'Moscow'})
        self.client.cookies = SimpleCookie({'user_city': 'Moscow'})
        # print(response.get('.city'))
        # response = self.client.get('/vote/2')
        self.assertEqual(response.status_code, 301)
        self.assertIn('Moscow', str(self.client.cookies))

    def test_register(self):
        print("url /register")
        response =self.client.post('/register/', )
        self.assertEqual(response.status_code, 200)
        
    def test_create(self):
        print("url /create")
        response =self.client.get('/add_data_db/')
        response =self.client.post('/create/', {
            "username": "kap", 
            "email": "kap@gmail.com", 
            "password": "1234c",
            "confirm_password": "1234c" })   
        print('RESPONSE: ',response)     
        # self.assertContains(response, "New Profile Creates Successfully!", html=True)

    def test_login(self):
        print("url /login")
        # response = self.client.get('/login/')
        response = self.client.post("/login/", {"username": "kek", "password": "1234p"})
        self.assertEqual(response.status_code, 200)
        # проверка редиректа
        # self.assertEqual(response.url, '/')

class TestAppModels(TestCase):

    def test_model_categories(self):
        print("model Categories")
        category = Categories.objects.create(category='White', fermentation='7-10 %')
        self.assertIn("White", str(category))

    def test_model_Type_packaging(self):
        print("model Type_packaging")
        type_packaging = ['Loose', 'Sphere', 'Сake', 'Bowl', 'Brick']
        for obj in type_packaging:
            packaging_row = Type_packaging.objects.create(packaging=obj)
            self.assertEqual(obj, str(packaging_row))
        
    def test_model_weight(self):
        print("model Weight")
        weights = [25, 40, 50, 75, 80, 100, 250, 357, 500]
        for obj in weights:
            weight_row = Weight.objects.create(weight=obj)
            self.assertEqual(obj, weight_row.weight)

    def test_model_tea(self):
        print("model Teas")
        teas = ['Yue Guang Bai (White Moonlight)',
                   'Bai Hao Yin Zhen, Yunnan',
                   'Lao Shou Mei',
                   'Xi Hu Longjing "Dragon Well'
        ]
        for obj in teas:
            tea_row = Teas.objects.create(name=obj)
            self.assertEqual(obj, tea_row.name)

    def test_model_products(self):
        print("model Products")
        tea = Teas.objects.create(name='Yue Guang Bai (White Moonlight)')
        category = Categories.objects.create(category='White', fermentation='7-10 %')
        packaging = Type_packaging.objects.create(packaging='Loose')
        product = Products.objects.create(
            tea_id = 1, 
            category_id = 1,
            description = 'Preety tea..',
            packaging_id = 1,
            image = '/tea/1.jpg'
        )
        self.assertEqual(tea.id, product.tea_id)

    def test_model_store(self):
        print("model Store")
        tea = Teas.objects.create(name='Yue Guang Bai (White Moonlight)')
        category = Categories.objects.create(category='White', fermentation='7-10 %')
        packaging = Type_packaging.objects.create(packaging='Loose')
        product = Products.objects.create(
            tea_id = 1, 
            category_id = 1,
            description = 'Preety tea..',
            packaging_id = 1,
            image = '/tea/1.jpg'
        )
        Weight.objects.create(weight=25)
        store = Store.objects.create(product_id = 1, weight_id = 1, amount = 4, price = 3.4)
        self.assertEqual(store.product_id, product.id)
        self.assertEqual(4, store.amount)
        self.assertEqual(3.4, store.price)
        self.assertIn('7-10 %', str(Categories.objects.all()))