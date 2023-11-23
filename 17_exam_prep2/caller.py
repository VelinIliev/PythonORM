import os
import random

import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Order, Product


# Import your models here
# Create and run your queries within functions


def get_profiles(search_string=None):
    if search_string is not None:
        profiles = Profile.objects \
            .annotate(num_orders=Count('orders')) \
            .filter(Q(full_name__icontains=search_string) |
                    Q(email__icontains=search_string) |
                    Q(phone_number__icontains=search_string)) \
            .order_by('full_name')

        if profiles:
            return '\n'.join(
                f'Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, '
                f'orders: {p.num_orders}'
                for p in profiles)
        else:
            return ''
    else:
        return ''


def get_loyal_profiles():
    loyal_profiles = Profile.objects.get_regular_customers()

    if loyal_profiles.exists():
        return '\n'.join(f'Profile: {lp.full_name}, orders: {lp.num_orders}' for lp in loyal_profiles)
    else:
        return ''


def get_last_sold_products():
    last_order = Order.objects.order_by('-creation_date').first()
    if last_order:
        products = last_order.products.all().order_by('name')
        return f"Last sold products: {', '.join(p.name for p in products)}"
    else:
        return ""


def get_top_products():
    output = ['Top products:', ]
    top_products = Product.objects.annotate(num_orders=Count('orders')) \
                       .filter(num_orders__gt=0) \
                       .order_by('-num_orders', 'name')[:5]

    if top_products:
        [output.append(f'{tp.name}, sold {tp.num_orders} times') for tp in top_products]
    else:
        return ''

    return '\n'.join(output)


def apply_discounts():
    num_of_updated_orders = \
        Order.objects.annotate(count_products=Count('products')) \
            .filter(count_products__gt=2, is_completed=False) \
            .update(total_price=F('total_price') * 0.9)

    return f"Discount applied to {num_of_updated_orders} orders."


def complete_order():
    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if order is None:
        return ""

    order.is_completed = True
    order.save()

    for product in order.products.all():
        product.in_stock -= 1
        if product.in_stock == 0:
            product.is_available = False
        product.save()

    return "Order has been completed!"


# print(Profile.objects.get_regular_customers())
# print(get_profiles('iv'))
# print(get_loyal_profiles())
# print(get_last_sold_products())
# print(get_top_products())
# print(apply_discounts())
# print(create_data())
# print(complete_order())
