import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models

from main_app.models import ArtworkGallery, Laptop


# Create and check models
# Run and print your queries

# 01. Artwork Gallery

def show_highest_rated_art():
    highest_rated_art = ArtworkGallery.objects.all().order_by('-rating', 'id').first()
    return f"{highest_rated_art.art_name} is the highest-rated art with a {highest_rated_art.rating} rating!"


def bulk_create_arts(first_art, second_art):
    ArtworkGallery.objects.bulk_create([
        first_art,
        second_art
    ])


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


# artwork1 = ArtworkGallery(artist_name="Vincent van Gogh", art_name="Starry Night", rating=4, price=1200000.0)
# artwork2 = ArtworkGallery(artist_name="Leonardo da Vinci", art_name="Mona Lisa", rating=5, price=1500000.0)
# artwork3 = ArtworkGallery.objects.create(artist_name="Leonardo da Vinci", art_name="Mona Lisa2", rating=5, price=1500000.0)
# artwork4 = ArtworkGallery.objects.create(artist_name="Leonardo da Vinci", art_name="Mona Lisa2", rating=-1, price=1500000.0)

# Bulk saves the instances
# bulk_create_arts(artwork1, artwork2)
# print(show_highest_rated_art())
# delete_negative_rated_arts()
# print(ArtworkGallery.objects.all())


# 02. Laptop

def show_the_most_expensive_laptop():
    mel = Laptop.objects.all().order_by('price', 'id').first()
    return f"{mel.brand} is the most expensive laptop available for {mel.price}$!"


def bulk_create_laptops(*args):
    Laptop.objects.bulk_create(*args)


def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=('Asus', 'Lenovo')).update(storage=512)


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=('Apple', 'Dell', 'Acer')).update(memory=16)


def update_operation_systems():
    Laptop.objects.filter(brand='Asus').update(operation_system='Windows')
    Laptop.objects.filter(brand='Apple').update(operation_system='MacOS')
    Laptop.objects.filter(brand__in=('Dell', 'Acer')).update(operation_system='Linux')
    Laptop.objects.filter(brand='Lenovo').update(operation_system='Chrome OS')


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


# laptop1 = Laptop(
#     brand='Asus',
#     processor='Intel Core i5',
#     memory=8,
#     storage=256,
#     operation_system='Windows',
#     price=899.99
# )
#
# laptop2 = Laptop(
#     brand='Apple',
#     processor='Apple M1',
#     memory=16,
#     storage=512,
#     operation_system='MacOS',
#     price=1399.99
#
# )
#
# laptop3 = Laptop(
#     brand='Lenovo',
#     processor='AMD Ryzen 7',
#     memory=12,
#     storage=512,
#     operation_system='Linux',
#     price=999.99,
# )
#
# laptops_to_create = [laptop1, laptop2, laptop3]
# bulk_create_laptops(laptops_to_create)

# update_to_512_GB_storage()
# update_operation_systems()
# update_to_16_GB_memory()
# delete_inexpensive_laptops()
# print(show_the_most_expensive_laptop())
