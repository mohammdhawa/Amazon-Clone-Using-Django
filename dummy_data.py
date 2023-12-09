import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from faker import Faker
import random
from products.models import Product, Brand, Review



def seed_brands(n):
    fake = Faker()
    
    images = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg',
              '6.jpg', '7.jpg', '8.jpg', '9.jpg', '10.jpeg',
              '11.jpg', '12.jpeg', '13.jpeg', '14.jpg',
              '15.jpeg', '16.jpeg', '17.jpg', '18.jpeg',
              '19.jpeg', '20.jpeg']

    for _ in range(n):
        Brand.objects.create(
            name = fake.name(),
            image = f"brand/{images[random.randint(0, 19)]}"
        )
    print(f"{n} Brands was added successfully")



def seed_products(n):

    fake = Faker()
    flag_types = ['New', 'Sale', 'Feature']
    brands = Brand.objects.all()
    images = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg',
              '6.jpg', '7.jpg', '8.jpg', '9.jpg', '10.jpeg',
              '11.jpg', '12.jpeg', '13.jpeg', '14.jpg',
              '15.jpeg', '16.jpeg', '17.jpg', '18.jpeg',
              '19.jpeg', '20.jpeg']

    for _ in range(n):
        Product.objects.create(
            name = fake.name(),
            flag = flag_types[random.randint(0,2)],
            price = round(random.uniform(10.99, 99.99), 2),
            image = f"product/{images[random.randint(0, 19)]}",
            sku = random.randint(100, 1000000),
            subtitle = fake.text(max_nb_chars=450),
            description = fake.text(max_nb_chars=3500),
            brand = brands[random.randint(0, len(brands)-1)],
        )
    print(f"{n} Products was added successfully")



def seed_Reviews(n):
    pass



seed_products(1200)