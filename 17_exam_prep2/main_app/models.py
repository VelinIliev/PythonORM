from django.core import validators
from django.db import models


class ProfileManager(models.Manager):
    def get_regular_customers(self):
        return (
            self.annotate(num_orders=models.Count('orders'))
            .filter(num_orders__gt=2)
            .order_by('-num_orders')
        )


class Profile(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[validators.MinLengthValidator(2), ]
    )
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return self.full_name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validators.MinValueValidator(0.01), ]
    )
    in_stock = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(0)]
    )
    is_available = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    profile = models.ForeignKey(to=Profile, related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(to=Product, related_name='orders')
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validators.MinValueValidator(0.01), ]
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
