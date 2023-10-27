import os
import django
from django.db import models

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Order


# Import your models here
# Create and run your queries within functions

def get_profiles(search_string=None):
    if search_string:
        profiles = Profile.objects.filter(
            models.Q(full_name__contains=search_string) |
            models.Q(email__contains=search_string) |
            models.Q(phone_number__contains=search_string)
        ).order_by('full_name')
        if profiles:
            return '\n'.join(
                f'Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.order_set.count()}'
                for p in profiles)
        else:
            return ''
    else:
        return ''


def get_loyal_profiles():
    loyal = Profile.objects.get_regular_customers()
    if loyal:
        return '\n'.join(f'Profile: {l.full_name}, orders: {l.order_set.count()}' for l in loyal)
    else:
        return ''


def get_last_sold_products():
    last_order = Order.objects.order_by('creation_date').last()
    products = last_order.products.all().order_by('name')
    return f'Last sold products:  {", ".join(p.name for p in products)}'


print(get_profiles('ve'))
print(get_loyal_profiles())
print(get_last_sold_products())

# TODO: NOT READY